"""Same-origin research prototype API. No clinical or emergency predictions."""
from pathlib import Path
import os,json,re,sqlite3,secrets,hashlib,hmac,time,threading
from collections import defaultdict,deque
from contextlib import contextmanager
from fastapi import FastAPI,Request,HTTPException
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel,Field,ConfigDict
ROOT=Path(__file__).resolve().parents[1];CONFIG=json.loads((ROOT/'project.json').read_text());DATA=json.loads((ROOT/'data/workspace.json').read_text())
DEBUG=os.environ.get('DEBUG','1')=='1';SECRET=os.environ.get('SECRET_KEY','local-development-key-change-before-hosting')
if not DEBUG and (len(SECRET)<40 or SECRET.startswith('local-development')):raise RuntimeError('Set a unique SECRET_KEY with at least 40 characters for production.')
STORE=Path(os.environ.get('DATA_DIR',str(ROOT/'runtime')));STORE.mkdir(parents=True,exist_ok=True);DB=STORE/'accounts.sqlite3'
@contextmanager
def db():
 c=sqlite3.connect(DB,timeout=10);c.row_factory=sqlite3.Row
 try:yield c;c.commit()
 finally:c.close()
with db() as c:
 c.executescript('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,username TEXT UNIQUE NOT NULL,password TEXT NOT NULL); CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY,user_id INTEGER NOT NULL,expires REAL NOT NULL);')
app=FastAPI(title=CONFIG['name'],description='Research prototype. No validated clinical or emergency prediction.')
app.add_middleware(SessionMiddleware,secret_key=SECRET,session_cookie='research_session',max_age=28800,same_site='lax',https_only=not DEBUG)
lock=threading.Lock();attempts=defaultdict(deque)
def limit(request):
 ip=request.client.host if request.client else 'unknown';now=time.time()
 with lock:
  q=attempts[ip]
  while q and q[0]<now-300:q.popleft()
  if len(q)>=20:raise HTTPException(429,'Too many attempts. Retry in five minutes.')
  q.append(now)
  if len(attempts)>10000:
   for k in list(attempts)[:5000]:
    if not attempts[k] or attempts[k][-1]<now-300:del attempts[k]
def tokenhash(t):return hashlib.sha256(t.encode()).hexdigest()
def current(request):
 sid=request.session.get('sid')
 if not sid:return None
 with db() as c:return c.execute('SELECT users.id,users.username FROM sessions JOIN users ON users.id=sessions.user_id WHERE sessions.token=? AND sessions.expires>?',(tokenhash(sid),time.time())).fetchone()
def csrf(request):
 value=request.session.get('csrf','');provided=request.headers.get('X-CSRFToken','')
 if not value or not hmac.compare_digest(value,provided):raise HTTPException(403,'Invalid CSRF token. Reload the sign-in page.')
def passwordhash(p):
 salt=secrets.token_bytes(16);return salt.hex()+':'+hashlib.pbkdf2_hmac('sha256',p.encode(),salt,600000).hex()
def matches(p,stored):
 try:salt,digest=stored.split(':');return hmac.compare_digest(digest,hashlib.pbkdf2_hmac('sha256',p.encode(),bytes.fromhex(salt),600000).hex())
 except (ValueError,TypeError):return False
def sign_in(request,user):
 old=request.session.get('sid')
 with db() as c:
  if old:c.execute('DELETE FROM sessions WHERE token=?',(tokenhash(old),))
  sid=secrets.token_urlsafe(32);c.execute('INSERT INTO sessions VALUES(?,?,?)',(tokenhash(sid),user['id'],time.time()+28800));c.execute('DELETE FROM sessions WHERE expires<?',(time.time(),))
 request.session.clear();request.session.update(sid=sid,csrf=secrets.token_urlsafe(32))
@app.middleware('http')
async def security(request:Request,call_next):
 if request.method in ['POST','PUT','PATCH']:
  body=await request.body()
  if len(body)>32768:return JSONResponse({'detail':'Request exceeds 32 KB.'},status_code=413)
 response=await call_next(request)
 response.headers['X-Content-Type-Options']='nosniff';response.headers['X-Frame-Options']='DENY';response.headers['Referrer-Policy']='same-origin'
 if request.url.path.startswith('/api/'):response.headers['Cache-Control']='no-store'
 return response
@app.get('/api/session')
def session(request:Request):
 if not request.session.get('csrf'):request.session['csrf']=secrets.token_urlsafe(32)
 u=current(request);return {'user':u['username'] if u else None,'csrf':request.session['csrf']}
class Credentials(BaseModel):
 model_config=ConfigDict(extra='forbid',strict=True)
 username:str=Field(min_length=3,max_length=40)
 password:str=Field(min_length=1,max_length=128)
class Registration(Credentials):
 password_confirm:str=Field(max_length=128)
 accepted_limits:bool
@app.post('/api/signup')
def signup(data:Registration,request:Request):
 csrf(request);limit(request)
 if not re.fullmatch(r'[A-Za-z0-9_]{3,40}',data.username):raise HTTPException(400,'Use 3–40 letters, digits or underscores for username.')
 if not data.accepted_limits:raise HTTPException(400,'Please acknowledge the research limits.')
 if data.password!=data.password_confirm:raise HTTPException(400,'Passwords do not match.')
 p=data.password
 if len(p)<12 or p.isdigit() or data.username.lower() in p.lower() or p.lower() in ['password12345','abcdefghijkl','123456789012']:raise HTTPException(400,'Choose a less predictable password of at least 12 characters.')
 try:
  with db() as c:
   cur=c.execute('INSERT INTO users(username,password) VALUES(?,?)',(data.username,passwordhash(p)));u={'id':cur.lastrowid,'username':data.username}
 except sqlite3.IntegrityError:raise HTTPException(400,'Username unavailable.')
 sign_in(request,u);return {'ok':True}
@app.post('/api/login')
def login(data:Credentials,request:Request):
 csrf(request);limit(request)
 with db() as c:u=c.execute('SELECT * FROM users WHERE username=?',(data.username,)).fetchone()
 # Equal-cost check for unknown usernames reduces a simple timing difference.
 if not u:hashlib.pbkdf2_hmac('sha256',data.password.encode(),b'unknown-user-salt',600000);raise HTTPException(400,'Incorrect username or password.')
 if not matches(data.password,u['password']):raise HTTPException(400,'Incorrect username or password.')
 sign_in(request,u);return {'ok':True}
@app.post('/api/logout')
def logout(request:Request):
 csrf(request);sid=request.session.get('sid')
 if sid:
  with db() as c:c.execute('DELETE FROM sessions WHERE token=?',(tokenhash(sid),))
 request.session.clear();return {'ok':True}
class VariantQuery(BaseModel):
 query:str=Field(min_length=1,max_length=200)
@app.post('/predict')
def predict(data:VariantQuery):
 if CONFIG['flood']:raise HTTPException(404,'Use the weather source endpoint.')
 key=lambda s:re.sub(r'\s+','',s.strip().lower())
 record=next((r for r in DATA['records'] if any(key(a)==key(data.query) for a in r['aliases'])),None)
 return {'record':record,'pathogenicity_prediction':None,'confidence':None,'status':'source_lookup_only','note':'Source classification is not an AI prediction. No validated classifier is deployed.'}
@app.get('/risk/{district}')
def risk(district:str):
 if not CONFIG['flood']:raise HTTPException(404,'Use the variant source endpoint.')
 city=next((c for c in DATA['locations'] if c['name'].casefold()==district.casefold()),None)
 if not city:raise HTTPException(404,'Only eight city reference points are included, not all districts.')
 return {'city':city['name'],'snapshot':DATA['snapshot'],'weather':city['rows'],'dengue_probability':None,'flood_probability':None,'status':'weather_snapshot_only','note':'Not an official warning; no validated health or flood risk predictor.'}
@app.get('/health')
def health():return {'status':'ok','edition':'research prototype','public_predictions':False}
@app.get('/',response_class=HTMLResponse)
def home():return page('index')
@app.get('/{name}.html',response_class=HTMLResponse)
def page(name:str):
 if name not in ['index','login','signup','dashboard']:raise HTTPException(404,'Page not found.')
 return (ROOT/(name+'.html')).read_text().replace('data-backend="0"','data-backend="1"',1)
app.mount('/assets',StaticFiles(directory=ROOT/'assets'),name='assets')
(ROOT/'downloads').mkdir(exist_ok=True)
app.mount('/downloads',StaticFiles(directory=ROOT/'downloads'),name='downloads')
