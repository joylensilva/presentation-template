# Forma — raiz independente para apresentações

Esta pasta **presentation-template/** é a raiz da solução e o diretório de trabalho dos agentes.
Ela pode ser copiada ou aberta sozinha. A pasta experimental que a originou não
é workspace, dependência nem contexto necessário para novos projetos.

## Primeira ação de cada agente
Execute `python3 tools/prepare.py`. Ele prepara/revalida bytecode otimizado nível 1
em `.cache/python/`, local e descartável. Depois use `python3 tools/run.py ...`.
Não distribua `.cache/`, `__pycache__/` ou `.pyc`. Antes de entregar uma cópia da
raiz, execute `python3 tools/prepare.py --clean`; o próximo agente prepara de novo.

## Identidade visual aprovada
Signal Light foi aprovado pelo usuário (“Ficou boa.”) e aplicado aos dois presets.
Fonte canônica: `tools/styles/signal-light.css`, incorporada após a base estrutural.
`previews/` conserva o histórico de avaliação, não é dependência dos catálogos.
Mudanças futuras de identidade devem novamente ser propostas antes de promovidas.

## Regra principal
**O arquivo final é UM HTML AUTOCONTIDO.** CSS, JavaScript de PPTX, impressão,
apresentação e navegação devem estar dentro dele. `tools/` existe só para
manutenção/build/testes. Nunca entregue `<script src>`, CSS externo, `fetch`, CDN,
imagens de fundo ou uma pasta de assets necessária para abrir a apresentação.
Links de bibliografia são permitidos; dependências de execução não são.

## Comece aqui — leia apenas o necessário
1. Para qualquer apresentação: leia `BRIEF.md`, `STORYBOARD.md` e `SESSION.json`.
2. Escolha UMA skill na tabela abaixo e siga seus passos.
3. Leia um fragmento de `slides/` por vez. Não carregue o runtime para editar texto.
4. Mantenha HTML 1280×720, notas por slide e objetos PPTX editáveis.
5. Edite fontes, gere o HTML, execute os checks pertinentes e registre evidências.

| Tarefa | Skill em tools/ |
|---|---|
| Criar apresentação / adaptar conteúdo | [`author-slides`](tools/skills/author-slides/SKILL.md) |
| Corrigir layout / overflow | [`repair-layout`](tools/skills/repair-layout/SKILL.md) |
| Alterar formas / exportador PPTX | [`maintain-pptx`](tools/skills/maintain-pptx/SKILL.md) |
| Impressão / tela cheia / navegação | [`print-present`](tools/skills/print-present/SKILL.md) |
| Validar / preparar entrega | [`validate-release`](tools/skills/validate-release/SKILL.md) |
| Retomar com pouco contexto | [`resume-work`](tools/skills/resume-work/SKILL.md) |

## Fonte de verdade
- `src/general/project.json` + `src/general/slides/`: preset geral padrão (21 layouts).
- `src/project.json` + `src/slides/`: preset educacional opcional (21 layouts).
- `projects/<projeto>/project.json` + `slides/`: apresentação em produção.
- `tools/styles/` e `tools/runtime/`: códigos reutilizáveis.
- `tools/bundle.json`: ordem de incorporação. Não é uma lista de dependências finais.
- `template-apresentacoes.html`: catálogo geral compilado com Signal Light.
- `template-aulas.html`: catálogo educacional compilado com Signal Light.
- `SDD.md`: requisitos e critérios de aceite; leia só a seção afetada.

Ao generalizar, preserve todos os tipos de exemplo. O equivalente de `docente`
é `apresentador`; os demais tipos também existem no preset geral. Não reduza o
catálogo para simplificar o domínio. `structure` e os testes verificam essa cobertura.

## Comandos — a partir desta pasta
```bash
python3 tools/prepare.py
python3 tools/run.py doctor
python3 tools/run.py inspect --catalog
python3 tools/run.py build
python3 tools/run.py build --check
python3 tools/run.py standalone
python3 tools/run.py validate --strict
```
Para um projeto, passe `--project projects/<projeto>/project.json` ao build e o caminho
do HTML a `self_contained.py`/`validate.py`. Comandos completos em `docs/COMMANDS.md`.

## Protocolo de contexto curto
Faça uma tarefa e 1–3 slides por rodada. Ao parar, atualize `SESSION.json` com
arquivos alterados, resultado dos comandos e próxima ação exata. Não releia tudo.
Use `tools/context_pack.py --task author --project <manifesto> --slide 1`.
Não reimplemente o exportador para escrever conteúdo. Não invente fontes. Aulas,
pitchs, propostas, apresentações técnicas e executivas usam o mesmo motor.

## Conclusão verificável
Não chame `integration-test-only.pptx` de entregável: ele contém uma mutação de teste.
Exporte o PPTX original com `tools/export_pptx.py` quando solicitado. O HTML deve
abrir sozinho fora desta pasta. Declare checks não executados ou ferramentas
ausentes; LibreOffice não comprova teste no Microsoft PowerPoint. Fullscreen
com clique real exige revisão manual; o headless testa o fallback em janela.
