---
name: repair-layout
description: Use quando houver desalinhamento, texto cortado, overflow ou divergência visual em um slide Forma.
---
# Corrigir um layout

1. Leia o requisito visual e UM fragmento (`tools/inspect_slides.py --slide N`).
   Com `--project`, selecione a aula correta.
2. Reproduza antes de alterar:
   ```bash
   python3 tools/screenshot.py projects/aula-01/apresentacao.html --slide 2 --output artifacts/antes.png
   ```
3. Decida a menor fonte a editar: fragmento, CSS local da aula ou estilo compartilhado.
   Conteúdo de uma aula não deve mudar o catálogo global.
4. Prefira flex/grid e alinhamento de caixas. Não use espaços de texto para posicionar.
   Para checklists, centralize o ícone na caixa e a caixa junto do bloco de texto.
5. Recompile, execute `self_contained.py`, `validate.py` e capture o mesmo slide.
6. Leia a imagem; um PNG gerado não comprova alinhamento sem inspeção.

## Arquivos úteis
- `tools/styles/theme.css`: estrutura dos componentes.
- `tools/styles/signal-light.css`: identidade aprovada e cores atuais.
- `tools/styles/print.css`: impressão.
- `docs/CONTRACT.md`: recursos vetoriais suportados.
- `docs/KNOWLEDGE.md`: lições de checkbox, medidas e diferenças de renderização.

## Limites
Não rasterize a correção. Não use pseudo-elemento para conteúdo visual, sombra,
transformação ou imagem de fundo. Não reduza todas as fontes para fazer um slide
denso caber: divida-o. Preserve 1280×720 e rodapé.

## Entrega
Registre causa, arquivos, número do slide e capturas antes/depois. Se o CSS é
compartilhado, inspecione também os outros layouts afetados. Não repita a suíte
completa sem nova alteração/falha que justifique.
