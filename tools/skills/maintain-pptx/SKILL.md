---
name: maintain-pptx
description: Use quando for corrigir ou estender a conversão HTML para formas e textos editáveis do PowerPoint.
---
# Manter o exportador editável

Não use esta skill para apenas trocar textos de uma aula.

1. Leia os requisitos PPTX em `SDD.md` e o contrato em `docs/CONTRACT.md`.
2. Escolha o arquivo mínimo:
   - `tools/runtime/pptx-drawing.js`: geometria, texto, preenchimento e links;
   - `tools/runtime/pptx-dom.js`: medição, diagnóstico e percurso DOM;
   - `tools/runtime/pptx-package.js`: OOXML, mestres, tema e notas;
   - `tools/runtime/zip.js`: CRC32 e ZIP STORE;
   - `tools/runtime/export-pptx.js`: download/feedback;
   - `tools/runtime/bootstrap.js`: API pública.
3. Escreva um caso reproduzível pequeno ANTES de alterar o algoritmo. Preserve
   `AulaTemplate.exportPptx({download:false})` → `Uint8Array` e `validate()` → lista.
4. Corrija o mapeamento equivalente. Elemento sem suporte deve gerar diagnóstico,
   nunca screenshot, imagem ou desaparecimento silencioso.
5. Recompile e teste:
   ```bash
   python3 tools/build.py
   python3 -m unittest discover -s tools/tests -v
   python3 tools/validate.py --strict
   python3 tools/export_pptx.py --output artifacts/original.pptx
   python3 tools/render_office.py artifacts/original.pptx --output artifacts/original-office.pdf --strict
   ```
6. Compare visualmente HTML/PDF e PPTX renderizado nos layouts afetados.

## Invariantes
9525 EMU por pixel. Slide = 12192000×6858000 EMU. Texto em linhas editáveis,
font-size CSS px × 75 = OOXML em centésimos de ponto. Notas não aparecem no slide.
ZIP/XML válidos não substituem abertura no Office. Não afirme teste no PowerPoint
quando só LibreOffice foi usado. Atualize `SDD.md`/contrato se o suporte mudou.
