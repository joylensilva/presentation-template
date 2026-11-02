# Fontes dos presets de apresentações

`general/` é o preset padrão, agnóstico de domínio. `project.json` + `slides/`
na raiz de src/ conservam o preset educacional opcional. O motor é compartilhado.
Não aplique a direção visual de previews/ sem aprovação explícita do usuário.
Signal Light já foi aprovado e está em `../tools/styles/signal-light.css`.
`components/signal-board.html` é expandido pelo marcador `<!-- FORMA:SIGNAL_ART -->`
nos fragmentos; o HTML final contém todos os elementos reais, sem includes externos.

Cada arquivo de `slides/` contém UM slide e seu comentário GUIA. Leia e edite
somente o layout relevante. A ordem do catálogo está em `project.json`.

- Novos projetos: use `python3 tools/run.py new`; padrão general; `--preset education`
  seleciona aulas. Não personalize os catálogos com conteúdo de um cliente/turma.
- Preserve `class="slide"`, `data-layout`, `data-title` e `speaker-notes`.
- `shell.html` tem marcadores de build; não é um entregável pronto para abrir.
- Se adicionar um layout, atualize `catalog.json` e `project.json` juntos.
- Estilos reutilizáveis ficam em `../tools/styles/theme.css`; impressão em `print.css`.
- O HTML final é autocontido. Use `tools/build.py`; não transforme marcadores em links.
