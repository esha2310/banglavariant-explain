# Sources and attribution

Snapshot 2026-10-17. Source records are frozen and may change.
- NCBI ClinVar: https://www.ncbi.nlm.nih.gov/clinvar/ . Exact VCV records 17677 (BRCA1), 15442 (HBB), 7105 (CFTR). Raw VCV XML responses retained in data/. Source accession version, classification, review, last evaluated and update dates remain separate. Documentation: https://www.ncbi.nlm.nih.gov/clinvar/docs/maintenance_use/ . ClinVar aggregates submitted assertions; this app adds no new classification. Data reuse/NCBI disclaimer: https://www.ncbi.nlm.nih.gov/home/about/policies/ . Third-party submitted content may have its own terms; original code licence does not grant rights over data.
- Europe PMC API query: `(BRCA1 OR "hemoglobin E" OR CFTR) AND OPEN_ACCESS:Y AND LICENSE:"cc by"`, core results, page size 12. Twelve records explicitly marked `cc by` with first publication dates no later than snapshot are bundled. Full source response data/literature.json; derived titles, authors, dates, DOI, URL and abstracts in workspace.json. Attribution remains on each displayed article. Abstract cleaning strips markup only. No comprehensive, systematic or variant-level evidence collection is claimed.
- ClinGen guidance link: https://www.clinicalgenome.org/tools/clingen-variant-classification-guidance/ . No claim of implementing ACMG/AMP expert classification.
- gnomAD ancestry documentation link: https://gnomad.broadinstitute.org/help/ancestry . No frequency data, ancestry representation percentage or Bangladesh-specific result is imported.
- Hero artwork: original AI-generated decorative violet/cyan DNA concept. Not a scientific model, experimental image or data visualization. Generated with the built-in image tool. Prompt retained in assets/PROMPT.txt.

No source endorsement or affiliation. Original code licence is separate from public data/abstract licences. Each article's authors and licence must remain attributed when redistributing.
