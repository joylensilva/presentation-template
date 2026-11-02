---
name: resume-work
description: Use ao retomar uma tarefa de apresentação com contexto limitado ou transferir trabalho entre agentes locais e remotos.
---
# Retomar sem reler tudo

A raiz é a própria pasta presentation-template/. Primeira ação: `python3 tools/prepare.py`.
Use `python3 tools/run.py` para os CLIs; o cache gerado localmente não é distribuído.
Se SESSION.json indicar pending_visual_approval, peça o feedback e não promova
o tema de previews/ aos estilos compartilhados por conta própria.

1. Leia `AGENTS.md` e o `SESSION.json` do projeto.
2. Identifique `goal`, `phase`, `next_slide`, `blockers` e `next_action`.
3. Abra somente o brief e a skill da próxima tarefa. Para gerar um pacote curto:
   ```bash
   python3 tools/context_pack.py --task author --project projects/aula-01/project.json --slide 3 --output artifacts/contexto.md
   ```
4. Não infira conteúdo de arquivos omitidos. Leia-os só se a tarefa depende deles.
5. Antes de escrever, confira a fonte do slide. Depois do patch, recompile.
6. Trabalhe em 1–3 slides ou em um único comportamento do runtime por rodada.
7. Antes de encerrar, atualize SESSION.json:
   - objetivo e fase atuais;
   - arquivos realmente alterados;
   - checks executados, resultado e caminho dos relatórios;
   - bloqueios concretos;
   - próxima ação exata e slide-alvo.

## Memória confiável
Specs e arquivos são a fonte da verdade; resumos podem estar desatualizados.
Não trate um teste antigo como prova após novas mudanças. Não reabra todos os
scripts para produzir conteúdo. Não reescreva o motor PPTX por falta de contexto.
O entregável segue sendo um HTML autocontido, mesmo que as fontes sejam modulares.
