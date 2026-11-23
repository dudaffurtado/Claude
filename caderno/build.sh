#!/usr/bin/env bash
# Valida, monta o HTML e gera o PDF do caderno. Uso: bash caderno/build.sh [--meta]
set -euo pipefail
cd "$(dirname "$0")"
python3 validar.py dados/*.yaml "$@"
python3 render.py saida/caderno.html dados/*.yaml
node -e "
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+process.cwd()+'/saida/caderno.html');
await p.pdf({path:'saida/SEFAZ-RS_AFRE_Caderno_de_Questoes.pdf',format:'A4',preferCSSPageSize:true,printBackground:true});
await b.close();})()"
# primeira página: "Meu progresso" (gerada em capas/)
if [ -f capas/progresso.pdf ]; then
  pdfunite capas/progresso.pdf saida/SEFAZ-RS_AFRE_Caderno_de_Questoes.pdf saida/tmp.pdf && mv saida/tmp.pdf saida/SEFAZ-RS_AFRE_Caderno_de_Questoes.pdf
fi
pdfinfo saida/SEFAZ-RS_AFRE_Caderno_de_Questoes.pdf | grep Pages
