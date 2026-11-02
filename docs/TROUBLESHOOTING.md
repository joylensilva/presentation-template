# Diagnóstico rápido

- **Raiz nova:** abra presentation-template/ diretamente. Nenhuma ferramenta precisa do pai.
- **Bytecode:** execute `tools/prepare.py` na primeira rodada e `tools/run.py`
  para os CLIs. Cache fica em .cache/python; limpe com prepare.py --clean antes
  de distribuir a solução. Não use pyc pré-gerado de outra máquina.
- **Visual atual:** Signal Light aprovado em tools/styles/signal-light.css.
  Prévias são histórico; não devem ser dependências do build de produção.

| Sintoma | Ação mínima |
|---|---|
| HTML desatualizado | Rode build; use `--check` para conferir |
| Mudança desapareceu | Edite fontes do projeto, não o compilado |
| Sem API / relatório JS não termina | Confira sintaxe e ordem em bundle.json; runtime completo precisa ser embutido |
| Script ou CSS externo detectado | Use build; não troque os slots por links |
| Exportação interrompida | Leia slide/elemento do diagnóstico; corrija o recurso sem suporte |
| Overflow/corte | Reduza conteúdo ou divida o slide; reveja largura e alinhamento |
| PPTX abre com reparo | Rode validate_pptx e examine content types/rels/IDs; depois render_office |
| Fonte quebra de outro jeito | Instale a mesma fonte no destino e compare as linhas; não rasterize |
| PDF só imprime slide ativo | @media print deve exibir todas as seções e remover transform |
| PDF com página extra | Confira altura 720px, margens zero e último break-after |
| Fullscreen recusado | Use fallback em janela; teste com clique real no navegador |
| Teste sem LibreOffice/pdfinfo | Instale a ferramenta de teste ou registre skip; --strict exige ambas |
| Conteúdo da capa aparece como FORMA42 | Você abriu o PPTX de integração; gere export original |
| Projeto tem menos de 21 slides | Isso é válido; testes genéricos precisam usar contagem dinâmica |

## Navegador headless

`FORMA_BROWSER` ou `--browser` permite selecionar Brave/Chromium. No ambiente
validado, Brave 156 travou com um `--user-data-dir` explícito recém-criado.
O fluxo usa o perfil temporário criado pelo próprio headless. Não aponte os
testes para o perfil interativo do usuário.

As ferramentas aplicam timeout e encerram somente o grupo do processo que
iniciaram. Não use comandos amplos para matar todos os processos Brave/Office.
Mensagens `dbind` de acessibilidade e `javaldx` de Java foram observadas sem
impedir exportação; o critério é a saída nova existente e validada, não só stderr vazio.

## Antes de ampliar o contexto

Registre: comando, código de saída, slide, elemento e caminho do relatório.
Leia apenas a skill e o módulo ligados a esse diagnóstico. Não mude o contrato
ou desative checks para transformar uma falha em aprovação.
