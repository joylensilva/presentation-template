# Comandos canônicos

`presentation-template/` é a raiz independente: execute os agentes e comandos nela, mesmo
depois de copiá-la para outro local. Não é necessário abrir o experimento pai.
Use caminhos entre aspas se houver espaços.
Manifestos resolvem seus caminhos relativamente ao arquivo `project.json`.

## Primeira rodada — bytecode local, não distribuído
```bash
python3 tools/prepare.py
python3 tools/run.py doctor --strict
```
`run.py` prepara/revalida automaticamente o cache e usa Python `-O`, com bytecode
em `.cache/python/`. Os scripts diretos listados abaixo seguem compatíveis; o
executor é o fluxo recomendado. Ex.: `tools/run.py build`, `new`, `inspect`,
`context`, `standalone`, `structure`, `test`, `validate`, `export`, `print`, `office`.

Antes de distribuir/copiar a raiz limpa:
```bash
python3 tools/prepare.py --clean
```

## Ambiente e catálogo
```bash
python3 tools/doctor.py --strict
python3 tools/inspect_slides.py --catalog
python3 tools/inspect_slides.py --layout comparacao
```

## Nova aula e contexto econômico
```bash
python3 tools/new_presentation.py --directory projects/aula-01 --title "Minha apresentação" --layouts capa objetivos conceito comparacao dados sintese referencias encerramento
python3 tools/inspect_slides.py --project projects/aula-01/project.json
python3 tools/inspect_slides.py --project projects/aula-01/project.json --slide 3
python3 tools/context_pack.py --task author --project projects/aula-01/project.json --slide 3 --max-chars 16000 --output artifacts/contexto.md
```
Tarefas do context pack: `author`, `layout`, `export`, `print`, `test`, `resume`.
Saída informa arquivos omitidos; não corta silenciosamente o código de um slide.
O nome de diretório do exemplo é arbitrário: o preset padrão é general, com
contexto, decisão, proposta e evidências. Para aulas: `new --preset education`.

## Presets e histórico visual
```bash
python3 tools/run.py inspect --catalog --preset general
python3 tools/run.py inspect --catalog --preset education
python3 tools/run.py build --project previews/tech-v2/project.json
```
Padrão: `src/general/project.json` → `template-apresentacoes.html` (21 layouts).
Educacional: `src/project.json` → `template-aulas.html` (21 layouts).
Signal Light está aprovado e aplicado aos dois presets. Fonte canônica:
`tools/styles/signal-light.css`. `previews/tech-v2.html` conserva o histórico.

## Build
```bash
python3 tools/build.py
python3 tools/build.py --check
python3 tools/build.py --project projects/aula-01/project.json
python3 tools/build.py --project projects/aula-01/project.json --check
```
`--output outro.html` muda o destino. `--report arquivo.json` salva o hash/contagem.
Nenhum build gera `<script src>` ou `<link rel="stylesheet">` no entregável.

## Checks rápidos e completos
```bash
python3 tools/self_contained.py
python3 tools/check_structure.py
python3 -m unittest discover -s tools/tests -v
python3 tools/validate.py --strict
python3 tools/validate.py projects/aula-01/apresentacao.html --out artifacts/aula-01 --strict
```
`--strict` exige LibreOffice e pdfinfo. Sem ele, relatório explicita skips.
O pipeline salva `report.json`, PDF do HTML, PPTX de integração e render Office.
O PPTX de integração tem uma mutação de teste; não o distribua.

## Exportações de produção
```bash
python3 tools/export_pptx.py projects/aula-01/apresentacao.html --output artifacts/aula-01-original.pptx --report artifacts/pptx-export.json
python3 tools/validate_pptx.py artifacts/aula-01-original.pptx --report artifacts/pptx-structure.json
python3 tools/print_pdf.py projects/aula-01/apresentacao.html --output artifacts/aula-01-original.pdf --strict
python3 tools/render_office.py artifacts/aula-01-original.pptx --output artifacts/aula-01-office.pdf --strict
```

## Revisão visual
```bash
python3 tools/screenshot.py projects/aula-01/apresentacao.html --slide 3 --output artifacts/slide-03.png
python3 tools/contact_sheet.py artifacts/aula-01-original.pdf --out artifacts/visual-html
python3 tools/contact_sheet.py artifacts/aula-01-office.pdf --out artifacts/visual-pptx
```
Abra os `index.html` de revisão para comparar. Esses índices referenciam PNGs e
são **artefatos de teste**, não apresentações finais. Leia as imagens; não chame
a revisão visual de aprovada apenas porque um comando gerou PNGs.

## Navegador alternativo
Todos os comandos de navegador aceitam `--browser /caminho/executavel`.
Alternativamente, defina `FORMA_BROWSER` no ambiente. As ferramentas usam
headless e `--no-sandbox` para ambientes de teste conteinerizados; isso não é
uma configuração exigida para abrir a apresentação normalmente.

## Migrar a versão anterior (uma única vez)
```bash
python3 tools/import_legacy.py --input /caminho/template-aulas-anterior.html --destination /caminho/destino-vazio
```
Esse importador reconhece o catálogo original de 21 layouts e recusa sobrescrever
fontes. Não é um conversor genérico nem um passo necessário do build diário.
