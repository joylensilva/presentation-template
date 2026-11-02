---
name: author-slides
description: Use para criar apresentações gerais, propostas, pitchs, conteúdo técnico ou aulas no Forma, com HTML final autocontido.
---
# Criar uma apresentação

**Entrada:** tema, público, duração, objetivo/decisão e fontes. **Saída:** um HTML autocontido.
Comandos abaixo partem de `presentation-template/`.

Primeira rodada: `python3 tools/prepare.py`. Use `python3 tools/run.py` para os comandos.
O preset padrão é **general**. Aulas são opcionais com `--preset education`.
Ambos têm 21 exemplos. Se a tarefa é manter o catálogo, preserve todos os tipos;
em projetos específicos, selecione os layouts necessários ao brief.
Não promova o tema de `previews/` sem aprovação explícita do usuário.

1. Leia `AGENTS.md` e preencha `BRIEF.md`. Se faltam fatos essenciais, registre a
   lacuna; não invente conteúdo ou bibliografia.
2. Use `python3 tools/run.py inspect --catalog` para escolher layouts.
3. Crie fontes de uma nova apresentação:
   ```bash
   python3 tools/run.py new --directory projects/proposta-01 --title "Título da apresentação"
   ```
   Opcional: `--layouts capa objetivos comparacao dados sintese encerramento`.
4. Complete `projects/proposta-01/STORYBOARD.md` antes de escrever todos os slides.
5. Abra um fragmento por rodada:
   ```bash
   python3 tools/run.py inspect --project projects/proposta-01/project.json --slide 1
   ```
6. Edite 1–3 fragmentos; mantenha uma ideia por slide e notas do apresentador.
   Troque metadados em `project.json` E textos visíveis de capa/apresentador.
7. Gere e confira:
   ```bash
   python3 tools/run.py build --project projects/proposta-01/project.json
   python3 tools/run.py standalone projects/proposta-01/apresentacao.html
   ```
8. Use a skill `validate-release` ao concluir. Atualize `SESSION.json` a cada rodada.

## Leia sob demanda
- Componentes e limites: `docs/CONTRACT.md`.
- Cores do projeto: `projects/proposta-01/theme-overrides.css` (será embutido).
- Não leia/reescreva `tools/runtime/` para mudar conteúdo.

## Aceite
O HTML funciona sozinho, sem `src`, CSS, fontes ou assets externos. Todos os
controles estão internos. Texto cabe e é editável no PPTX. Fonte bibliográfica
é verificável. Conteúdo demonstrativo não foi confundido com fatos do projeto.
