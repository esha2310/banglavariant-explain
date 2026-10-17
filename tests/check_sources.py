from pathlib import Path
import json,hashlib,xml.etree.ElementTree as E,sys,subprocess
import numpy as np,joblib
from sklearn.metrics.pairwise import cosine_similarity
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R))
D=json.loads((R/'data/workspace.json').read_text());checks=json.loads((R/'data/SHA256.json').read_text())
for f,h in checks.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
for r in D['records']:
 raw=(R/'data'/f"{r['id']}.xml").read_bytes();a=E.fromstring(raw).find('VariationArchive');c=a.find('ClassifiedRecord/Classifications/GermlineClassification');assert c.findtext('Description')==r['classification'];assert c.findtext('ReviewStatus')==r['review'];assert hashlib.sha256(raw).hexdigest()==r['source_sha256'];assert r['south_asian_af'] is None
v=joblib.load(R/'ml/literature_tfidf.joblib');docs=v.transform([p['title']+' '+p['abstract'] for p in D['papers']]);queries=['BRCA1','hemoglobin E','CFTR','noquerytoken999'];expected=cosine_similarity(v.transform(queries),docs)
script="const fs=require('fs'),V=require('./frontend/engine.js').VariantEngine,D=JSON.parse(fs.readFileSync('data/workspace.json'));console.log(JSON.stringify("+json.dumps(queries)+".map(q=>{let v=V.vector(D,q);return D.tfidf.vectors.map(a=>v.reduce((s,x,j)=>s+x*a[j],0))})))"
actual=json.loads(subprocess.check_output(['node','-e',script],cwd=R,text=True));assert np.allclose(expected,actual,atol=1e-8)
print('Source hashes, exact ClinVar assertions and Python/JS TF-IDF agreement: PASS')
try:
 from pypdf import PdfReader
 pdf=R/'evidence/report_check.pdf'
 if pdf.exists():assert '17677' in '\n'.join(p.extract_text() for p in PdfReader(pdf).pages);print('PDF parsed and source accession text verified: PASS')
except ImportError:print('PDF parser unavailable; PDF text parse skipped.')
