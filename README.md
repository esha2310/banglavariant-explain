# BanglaVariant-Explain

A colourful bilingual research website by Nafisa Tasneem Esha. Flow: **Welcome → Login / Sign up / Guest → Dashboard**. Cinematic original AI-generated hero art, dark navy glass panels, responsive sidebar, source links and downloadable PDF.

## Honest release status
Actual ClinVar source lookup over three frozen records, exact build-aware VCF matching and TF-IDF retrieval over 12 CC BY abstracts. No trained pathogenicity classifier, gnomAD AF integration, South Asian clinical validation, SHAP or PubMedBERT/LLM RAG.

This is a research prototype, not a clinically validated or operational emergency-warning service. The source code implements the features stated below; it does not establish production readiness or scientific novelty. No invented accuracy, population representation percentages or confidence scores are displayed. The actual frontend is buildless HTML/CSS/JavaScript, not Next.js/React. The optional account backend is FastAPI.

## What works
- Four connected pages: welcome, login, signup and interactive dashboard.
- English/Bangla interface and explanations. Original scientific metadata/abstracts retain source language; no machine translation is presented as verified evidence.
- Source-linked data inspection and domain-specific browser tools.
- English PDF evidence export using built-in PDF writing. Uploaded local data excluded from PDF.
- Browser-local bookmarks, downloadable examples, source ZIP, documented methods and limitations.
- Real FastAPI signup, sign-in, sign-out, hashed passwords, CSRF checks, expiring/revocable sessions and basic process-local throttling when running the backend.

## Static public demo vs real accounts
**The public/GitHub Pages edition runs in Guest mode.** Login/signup pages are disabled previews and never collect passwords. The included FastAPI edition supports actual accounts. Do not describe the static demo as a hosted authentication service. Bookmarks remain browser-local even in account mode; no cross-device syncing or email/password-reset service exists.

## Open the website demo
Extract the website demo ZIP and keep `index.html`, `login.html`, `signup.html` and `dashboard.html` together. Open index.html. Assets are embedded in each page; optional Google Fonts require internet and have system-font fallbacks. Extract the full project to get source/data/scripts and a local backend.

## Windows / VS Code: one line at a time
Open the extracted project folder in VS Code → Terminal → New Terminal. The folder must contain requirements.txt and api/.
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn api.main:app --reload
```
Open http://127.0.0.1:8000/ . Keep terminal open. Signup creates a new local account; no default password. Stop with Ctrl+C. On Linux/macOS use `python3 -m venv .venv`, then `.venv/bin/python` in place of the Windows Python executable. The server creates runtime/accounts.sqlite3 (ignored by Git). No patient VCF/case data should be uploaded.

## Rebuild & checks
```sh
python build.py
node tests/check_engine.cjs
node tests/check_pages.cjs
python -m unittest tests.test_api
python tests/check_sources.py
```
Node is required for JavaScript checks only. See VALIDATION.md for tests actually run and remaining verification limits. Source responses and their hashes are included. Scientific claims need independent external evaluation; software tests are not accuracy evidence.

## GitHub Pages
Upload extracted files/folders preserving structure. Settings → Pages → Deploy from branch → main → /(root). Four HTML pages must remain together. `downloads/` provides the source ZIP. GitHub Pages cannot run FastAPI. See GITHUB_UPLOAD_BN.md and DEPLOYMENT.md.

## Data / privacy
Variant data: public ClinVar source records. Abstracts: 12 Europe PMC records marked CC BY, with title/author/date/link/attribution retained. This small convenience collection is not representative of South Asia.
Local upload tools process text in browser memory. App code does not send VCF or CSV contents to the backend or save them to disk. Hosting providers still receive regular requests/logs. Browser bookmarks contain only bundled record IDs or city/date settings. Account usernames and password hashes are stored in the backend database. Do not enter private genomes, health identifiers or confidential reports.

See DATA_SOURCES.md, MODEL_CARD.md, VALIDATION.md and DEMO_GUIDE_BN.md. Original code is MIT-licensed; data and artwork have separate terms in DATA_SOURCES.md. No external AI API key, paid model, SMS service or fake subscription is required.

## Refresh source snapshot
Run `python scripts/refresh_data.py`, `python ml/build_literature.py`, `python scripts/checksum.py`, then `python build.py`. Re-verify all source classifications and article licences. This does not train a pathogenicity classifier.
