"""Refresh the exact three public source records. No patient data or clinical prediction."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import urllib.request,urllib.parse,time,json,re,html,hashlib,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1];date=datetime.now(timezone(timedelta(hours=6))).date().isoformat();records=[]
for id in ['17677','15442','7105']:
 url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?'+urllib.parse.urlencode(dict(db='clinvar',id=id,rettype='vcv',is_variationid='true',retmode='xml'))
 with urllib.request.urlopen(url,timeout=40) as f:b=f.read()
 (R/'data'/f'{id}.xml').write_bytes(b);a=E.fromstring(b).find('VariationArchive');v=a.find('ClassifiedRecord/SimpleAllele');c=a.find('ClassifiedRecord/Classifications/GermlineClassification');gene=v.find('GeneList/Gene').get('Symbol');acc=a.get('Accession')+'.'+a.get('Version');name=a.get('VariationName');aliases=[name,id,a.get('Accession'),acc]+[x.text for x in v.findall('.//HGVS/NucleotideExpression/Expression') if x.text]
 if gene=='BRCA1':aliases+=['BRCA1 c.5266dupC','BRCA1 c.5266dup']
 if gene=='CFTR':aliases+=['CFTR F508del','CFTR c.1521_1523del']
 records.append(dict(id=id,accession=acc,name=name,gene=gene,type=v.findtext('VariantType'),classification=c.findtext('Description'),review=c.findtext('ReviewStatus'),evaluated=c.get('DateLastEvaluated'),updated=a.get('DateLastUpdated'),locations=[x.attrib for x in v.findall('Location/SequenceLocation')],aliases=aliases,consequences=sorted({x.get('Type') for x in v.findall('.//MolecularConsequence') if x.get('Type')}),pmids=list(dict.fromkeys(x.text for x in c.findall('.//Citation/ID') if x.get('Source')=='PubMed')),url=f'https://www.ncbi.nlm.nih.gov/clinvar/variation/{id}/',south_asian_af=None,global_af=None,ml_prediction=None,source_sha256=hashlib.sha256(b).hexdigest()));time.sleep(.4)
u='https://www.ebi.ac.uk/europepmc/webservices/rest/search?'+urllib.parse.urlencode({'query':'(BRCA1 OR "hemoglobin E" OR CFTR) AND OPEN_ACCESS:Y AND LICENSE:"cc by"','format':'json','resultType':'core','pageSize':12})
with urllib.request.urlopen(u,timeout=40) as f:b=f.read()
(R/'data/literature.json').write_bytes(b);raw=json.loads(b);papers=[]
for a in raw['resultList']['result']:
 if a.get('license','').lower()!='cc by' or a.get('firstPublicationDate','9999')>date:continue
 papers.append(dict(id=a.get('pmid') or a['id'],title=a['title'],authors=a.get('authorString',''),date=a.get('firstPublicationDate',''),abstract=html.unescape(re.sub('<[^>]*>',' ',a.get('abstractText',''))),doi=a.get('doi',''),license=a.get('license'),url='https://europepmc.org/article/'+a['source']+'/'+a['id']))
old=json.loads((R/'data/workspace.json').read_text());old.update(snapshot=date,records=records,papers=papers);old.pop('tfidf',None);(R/'data/workspace.json').write_text(json.dumps(old,ensure_ascii=False,separators=(',',':')))
print('Refreshed public records. Next run python ml/build_literature.py then python build.py. Re-check sources before use.')
