const fs=require('fs'),assert=require('assert'),V=require('../frontend/engine.js').VariantEngine,D=JSON.parse(fs.readFileSync('data/workspace.json'));
assert.equal(V.lookup(D,' BRCA1 c.5266dupC ').id,'17677');assert.equal(V.lookup(D,'BRCA1 c.5266dupT'),null);assert.equal(V.lookup(D,'BRCA1'),null);
for(const r of D.records){const l=r.locations.find(l=>l.Assembly==='GRCh38'),text='##fileformat=VCFv4.2\n##reference=GRCh38\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n'+[l.Chr,l.positionVCF,'.',l.referenceAlleleVCF,l.alternateAlleleVCF,'.','PASS','.'].join('\t');assert.equal(V.vcf(D,text,'GRCh38')[0].record.id,r.id);assert.throws(()=>V.vcf(D,text,'GRCh37'));assert.equal(V.vcf(D,text.replace('\t'+l.positionVCF+'\t','\t1\t'),'GRCh38')[0].record,null)}
assert.throws(()=>V.vcf(D,'garbage','GRCh38'));assert.equal(V.search(D,'zzzzunlikelyterm987').length,0);assert(V.search(D,'BRCA1').length>0);
for(const r of D.records){assert.equal(r.south_asian_af,null);assert.equal(r.ml_prediction,null)}
console.log('Variant engine exact lookup, build-aware VCF, invalid-input rejection, no fabricated predictions: PASS');
