# Deployment and account boundary

## Static demo / GitHub Pages / Sites
Serve the root four HTML pages with assets/ and downloads/. No build framework or API key needed. The public demo is Guest-only. Forms explicitly disable credential entry. No account or alert subscription is created in a static host.

## FastAPI with real accounts
Install requirements, run python build.py, set DATA_DIR to persistent storage and deploy `uvicorn api.main:app --host 0.0.0.0 --port 8000` behind your own HTTPS reverse proxy. Dockerfile is included. Set DEBUG=0 and a unique SECRET_KEY of at least 40 random characters. Environment files are not loaded automatically; set variables through your host or terminal. In production use HTTPS so secure cookies work. Persist and back up runtime data; never commit the database. Session secrets must remain private. Do not use --reload publicly.

Passwords use salted PBKDF2-HMAC-SHA256; the database stores only hashes and hashed session IDs. Session cookies are HTTP-only, SameSite=Lax and secure in production. CSRF tokens are required on signup/login/logout. Sessions expire after eight hours and logout revokes them server-side. No email verification, password reset, admin portal, MFA or cross-device bookmarks. Basic in-process throttling is not a distributed abuse-control system. SQLite and one process are sufficient for a small prototype, not a production scaling guarantee.

A full hosted account deployment needs operational review, shared rate limiting, database/backups, monitoring and your own privacy/retention process. The provided public URL publishes static Guest analysis, not the FastAPI service. Free-host limits, uptime and pricing can change; no permanent free availability or Lighthouse score is promised. Browser visual/mobile QA remains to be done.
