import os,tempfile,unittest,sqlite3
os.environ['DATA_DIR']=tempfile.mkdtemp(prefix='research-tests-');os.environ['DEBUG']='1'
from fastapi.testclient import TestClient
from api.main import app,DB,CONFIG,DATA,attempts
class APITests(unittest.TestCase):
 def setUp(self):
  attempts.clear();self.c=TestClient(app)
 def token(self):return self.c.get('/api/session').json()['csrf']
 def post(self,url,d):return self.c.post(url,json=d,headers={'X-CSRFToken':self.token()})
 def test_pages(self):
  for name in ['index','login','signup','dashboard']:
   r=self.c.get('/'+name+'.html');self.assertEqual(r.status_code,200);self.assertIn('data-backend="1"',r.text)
  self.assertEqual(self.c.get('/not-a-page.html').status_code,404)
 def test_csrf(self):
  self.assertEqual(self.c.post('/api/login',json={'username':'abc','password':'bad'}).status_code,403)
  self.assertEqual(self.c.get('/api/logout').status_code,405)
 def test_account_flow(self):
  name='u'+os.urandom(5).hex();p='River$Forest58!moon'
  self.assertEqual(self.post('/api/signup',{'username':name,'password':p,'password_confirm':p,'accepted_limits':True}).status_code,200)
  self.assertEqual(self.c.get('/api/session').json()['user'],name)
  with sqlite3.connect(DB) as con:stored=con.execute('SELECT password FROM users WHERE username=?',(name,)).fetchone()[0]
  self.assertNotEqual(stored,p);self.assertEqual(self.post('/api/logout',{}).status_code,200);self.assertIsNone(self.c.get('/api/session').json()['user'])
  self.assertEqual(self.post('/api/login',{'username':name,'password':'wrong'}).status_code,400)
  self.assertEqual(self.post('/api/login',{'username':name,'password':p}).status_code,200)
 def test_weak_password(self):
  self.assertEqual(self.post('/api/signup',{'username':'shorttest','password':'123','password_confirm':'123','accepted_limits':True}).status_code,400)
 def test_domain_no_fake_prediction(self):
  if CONFIG['flood']:
   d=self.c.get('/risk/Dhaka').json();self.assertIsNone(d['flood_probability']);self.assertIsNone(d['dengue_probability']);self.assertEqual(self.c.get('/risk/nonexistent').status_code,404)
  else:
   d=self.c.post('/predict',json={'query':'BRCA1 c.5266dupC'}).json();self.assertEqual(d['record']['id'],'17677');self.assertIsNone(d['confidence']);self.assertIsNone(d['pathogenicity_prediction'])
   d=self.c.post('/predict',json={'query':'unknown'}).json();self.assertIsNone(d['record'])
if __name__=='__main__':unittest.main()
