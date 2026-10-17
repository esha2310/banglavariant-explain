from pathlib import Path
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
R=Path(__file__).resolve().parents[1];p=R/'data/workspace.json';d=json.loads(p.read_text());v=TfidfVectorizer(stop_words='english',max_features=2000);X=v.fit_transform([a['title']+' '+a['abstract'] for a in d['papers']]);d['tfidf']={'vocab':{k:int(i) for k,i in v.vocabulary_.items()},'idf':v.idf_.tolist(),'vectors':X.toarray().round(10).tolist(),'stopwords':sorted(v.get_stop_words())};p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')));joblib.dump(v,R/'ml/literature_tfidf.joblib',compress=3);print('Fitted TF-IDF corpus:',len(d['papers']),'abstracts. Not a pathogenicity classifier.')
