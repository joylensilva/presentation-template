---
name: print-present
description: Use quando for alterar impressão 16:9, tela cheia, navegação ou controles superiores do template Forma.
---
# Impressão e apresentação

1. Identifique o comportamento e o critério de aceite em `SDD.md`.
2. Leia só o arquivo afetado:
   - impressão: `tools/styles/print.css` + `tools/runtime/print.js`;
   - fullscreen: `tools/runtime/presentation.js`;
   - navegação/resize/notas: `tools/runtime/viewer.js`;
   - barra superior: `src/shell.html` + `tools/styles/theme.css`.
3. Preserve a prancheta 1280×720. Em tela, ajuste por escala uniforme, sem esticar.
   Em impressão, remova o transform e mostre TODOS os slides, um por página.
4. Não imprima controles, notas privadas ou área de medição do PPTX.
5. Recompile e execute:
   ```bash
   python3 tools/build.py
   python3 tools/print_pdf.py --output artifacts/impressao.pdf --strict
   python3 tools/validate.py --strict
   ```
6. Manualmente: clique em Apresentar; confirme fullscreen, passagem por setas,
   aparecimento dos controles no topo e saída com Esc. Teste também janela estreita.

## Medidas
Página = 13⅓×7½ pol = 960×540 pt. Margens zero. Último slide sem página vazia.
O headless testa o fallback quando Fullscreen API é recusada; isso NÃO comprova
fullscreen com um clique real. Registre os dois resultados separadamente.
