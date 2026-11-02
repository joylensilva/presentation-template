---
description: Cria uma apresentação Forma geral ou educacional, com brief e HTML autocontido.
---
Leia AGENTS.md e tools/skills/author-slides/SKILL.md. Pedido: $ARGUMENTS

Primeiro identifique público, duração, objetivos e fontes; registre lacunas.
Comece por python3 tools/prepare.py nesta raiz independente. General é o preset
padrão; use education somente para aulas. Aguarde aprovação visual antes de
promover o estilo de previews/ aos temas compartilhados.
Crie um projeto por tools/new_presentation.py, mantenha fontes em slides separados
e gere o entregável com tools/build.py. CSS e todo o runtime devem ficar embutidos
no HTML final. Trabalhe em blocos de até três slides e atualize SESSION.json.
