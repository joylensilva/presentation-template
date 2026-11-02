# Registro de validação da estrutura consolidada

**Registro histórico do preset educacional (versão 1.0).** A raiz independente,
o preset geral padrão e a prévia visual em aprovação estão documentados em
[ROOT-AND-PREVIEW.md](ROOT-AND-PREVIEW.md).

Data: 2026-11-02. Ambiente: Linux, Python 3.12.3, Brave 156, LibreOffice e Poppler.
Este registro é uma evidência desta versão, não uma aprovação automática de
mudanças futuras. Reexecute os checks afetados depois de alterar fontes.

## Resultado

- Build determinístico e `build.py --check`: aprovado.
- Contrato estático: 21 slides, 21 notas, zero dependências externas.
- Bundle, catálogo, links locais e seis skills: consistentes.
- Testes unitários do tooling: 5 aprovados.
- Pipeline completo do catálogo com `--strict`: aprovado.
- Projeto independente de **um slide**, build e pipeline `--strict`: aprovado.
- Export original: 21 slides, **584 formas, 399 caixas de texto, 18 conectores,
  21 notas, 2 links e zero imagens**, em 97 partes ZIP.
- HTML impresso e PPTX original renderizado no LibreOffice: 21 páginas 960×540 pt.
- Pacote de contexto do projeto de um slide: 7.617 caracteres, sem arquivos omitidos.
- Captura de tela e índices visuais: gerados; na reorganização, foram inspecionados
  os layouts 11 (diagrama) e 16 (código) para conferir a extração modular.
- A inspeção visual inicial do catálogo de 21 layouts foi feita antes da reorganização.

O PPTX de integração tem 583 formas e 398 textos porque a capa foi substituída
por uma única linha `FORMA42`. Essa diferença é esperada e é o motivo de separar
o arquivo de teste do export original.

Hash de inputs do catálogo validado:
`a6e41b4c0c4fea51f8d90db993ed34e5d4dec9e2ae688ac2186e66fb77deffaa`.

## Comandos executados

A partir de `presentation-template/`:

```bash
python3 tools/build.py
python3 tools/build.py --check
python3 tools/self_contained.py
python3 tools/check_structure.py
python3 -m unittest discover -s tools/tests -v
python3 tools/validate.py --out artifacts/catalog-validation --strict
python3 tools/export_pptx.py --output artifacts/catalog-original.pptx --report artifacts/catalog-export.json
python3 tools/render_office.py artifacts/catalog-original.pptx --output artifacts/catalog-original-office.pdf --strict
python3 tools/contact_sheet.py artifacts/catalog-original-office.pdf --out artifacts/visual-office
python3 tools/screenshot.py --slide 11 --output artifacts/slide-11.png
python3 tools/contact_sheet.py artifacts/catalog-validation/html-print.pdf --out artifacts/visual-html
```

Foi criado também `/tmp/opencode/forma-one-slide` com `new_presentation.py
--layouts capa`; seu build, impressão de uma página, PPTX editável, controles e
abertura Office passaram. O relatório está em `artifacts/one-slide-validation/report.json`.
Esse caminho temporário é do ambiente de validação, não uma dependência do template.

## Evidências geradas

- `artifacts/catalog-validation/report.json`
- `artifacts/one-slide-validation/report.json`
- `artifacts/catalog-export.json`
- `artifacts/catalog-original.pptx`
- `artifacts/catalog-original-office.pdf`
- `artifacts/visual-html/index.html` e `artifacts/visual-office/index.html`
- `artifacts/slide-11.png`
- `artifacts/one-slide-context.md`

Esses arquivos são artefatos regeneráveis e estão ignorados no versionamento.
O HTML final foi testado numa cópia temporária isolada, sem tools/src ao lado.

## Não executado nesta validação

- Abertura no Microsoft PowerPoint.
- Fullscreen com um clique real: o teste headless cobre a alternativa em janela.
- Benchmark de geração com modelos 12B/27B: a estrutura foi preparada para
  contexto curto, mas não houve medição de qualidade nesses modelos.
