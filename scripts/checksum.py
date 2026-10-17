from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]
d={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((R/'data').iterdir()) if p.is_file() and p.name!='SHA256.json'}
(R/'data/SHA256.json').write_text(json.dumps(d,indent=2))
print('Source checksum register rebuilt.')
