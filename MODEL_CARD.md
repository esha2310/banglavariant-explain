# Model / method card

Actual ClinVar source lookup over three frozen records, exact build-aware VCF matching and TF-IDF retrieval over 12 CC BY abstracts. No trained pathogenicity classifier, gnomAD AF integration, South Asian clinical validation, SHAP or PubMedBERT/LLM RAG.

## Implemented method
Exact identifier lookup on three ClinVar records. Source classifications and review status are reported separately from prediction; all three records are pathogenic convenience examples and cannot train/evaluate a binary classifier. HGVS conversion, fuzzy variant matching, liftover, left alignment, multiallelic decomposition and personal phenotype integration are not implemented. VCF lookup requires exact chromosome/position/REF/ALT in the selected build. Unmatched is not benign or VUS.

TF-IDF (English stopwords, 2,000 max features, L2 normalization) ranks twelve licensed titles/abstracts with cosine similarity. Zero vocabulary overlap returns no hit. No retrieval relevance benchmark, variant-specific entailment, PubMedBERT or generative LLM is implemented. Plain-language English/Bangla explanations are templates from source fields, not AI-derived medical conclusions.

No gnomAD AF/denominator, ancestry-labelled clinical cohort, CADD/REVEL, conservation score or supervised model is bundled. AUROC/AUPRC/confidence/SHAP are unavailable, never illustrative fake numbers. South Asian ancestry is not nationality and lower frequency is not automatically pathogenic. No arbitrary ancestry weighting is applied.

To study a classifier later: obtain appropriately licensed labels/features, define disease/variant scope and review criteria, avoid label-derived features and score circularity, split by gene and time before tuning, retain an external untouched cohort, audit ancestry coverage and calibration. No publishability or novelty claim follows from the current demo.

## Intended use / limits
Educational source inspection and reproducible software research only. No personal diagnosis, treatment, public-health decision or emergency action should rely on this prototype. Independent scientific evaluation and authorized representative data are required before operational claims.
