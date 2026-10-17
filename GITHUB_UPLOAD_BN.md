# BanglaVariant-Explain — GitHub upload

১. GitHub-ready ZIP → Extract All করুন। ভেতরের project folder খুলুন। ZIP নিজে upload করবেন না।
২. GitHub → New repository → নাম `banglavariant-explain` → Public → Create repository।
৩. Add file → Upload files → project-এর file ও folder একসঙ্গে drag করুন। `api`, `frontend`, `data`, `assets`, `ml`, `scripts`, `tests`, `downloads` folder অক্ষুণ্ণ রাখুন। শুধু ভেতরের file root-এ আলাদা করে তুলবেন না।
৪. `.venv`, `.env`, `runtime` বা ব্যক্তিগত data upload করবেন না। `.gitignore` এবং `.github` folder থাকলে রাখবেন।
৫. Description: `Source-linked genomic variant evidence explorer with bilingual context, build-aware VCF lookup and literature retrieval.`
৬. Commit message: `Add BanglaVariant-Explain research website and reproducible source` → Commit changes।
৭. Settings → Pages → Deploy from a branch → main → /(root) → Save। Public URL তৈরি হলে আলাদা browser/phone-এ পরীক্ষা করুন। Public demo-তে Guest ব্যবহার করবেন।
৮. আসল signup/login-এর জন্য FastAPI backend hosting দরকার। DEPLOYMENT.md পড়ুন। localhost link অন্যরা খুলতে পারবে না।

ফাইলের তথ্য বা description-এ validated clinical/emergency prediction, AUROC, LSTM/SHAP/RAG implemented—এমন দাবি করবেন না; যা run হয়নি তা future work।
