# Trabalho confortável com contexto limitado

Abra somente a raiz independente `presentation-template/`; o experimento pai não faz parte
do contexto necessário. Na primeira rodada execute `python3 tools/prepare.py`.
Use `tools/run.py` para reutilizar o bytecode local, sem distribuí-lo.
Apresentações gerais usam general; aulas usam o preset education opcional.
Durante a aprovação visual, não promova previews/ aos estilos compartilhados.

Esta organização reduz a carga de contexto para modelos locais, inclusive
12B/27B. Tamanho em parâmetros não garante qualidade ou janela de contexto;
ajuste o tamanho das rodadas ao modelo, quantização e configuração reais.

## Leitura progressiva

1. `AGENTS.md`: contrato mínimo e roteamento.
2. `SESSION.json`: ponto exato da retomada.
3. Uma skill da tarefa atual.
4. Brief e storyboard da aula.
5. Um fragmento de slide ou um módulo de runtime.

Não leia `template-aulas.html` inteiro para mudar um título. Não carregue todo
`tools/runtime/` para criar conteúdo. Use caminhos, não longas cópias repetidas.

## Pacotes curtos

```bash
python3 tools/context_pack.py --task author --project projects/aula-01/project.json --slide 3 --max-chars 12000 --output artifacts/contexto.md
```

O pacote contém instruções, uma skill, metadados, sessão, brief e um fragmento,
dentro do limite de caracteres. Arquivos que não cabem são listados, não cortados
no meio. O limite não é uma contagem exata de tokens. Abra um arquivo omitido
somente quando necessário e substitua contexto antigo em vez de acumular tudo.

## Rodadas sugeridas

| Situação | Unidade de trabalho |
|---|---|
| Modelo com menor capacidade / execução muito quantizada | Um slide ou uma alteração de componente |
| Modelo local com mais folga | Dois ou três slides relacionados |
| Exportador ou regra complexa | Um caso mínimo + um helper, seguido de teste |
| Revisão | Um problema comprovado + uma evidência antes/depois |

Prefira instruções literais: arquivo, trecho, resultado esperado e comando.
Evite pedir "reescreva todo o template" para resolver uma falha local.

## Checkpoint obrigatório

`SESSION.json` precisa ter:
- objetivo e fase;
- caminho do manifesto;
- próximo slide;
- arquivos realmente modificados;
- checks com comando e resultado/caminho do relatório;
- bloqueios concretos;
- próxima ação exata.

Exemplo de check: `{"command":"python3 tools/self_contained.py ...", "result":"pass", "report":"artifacts/..."}`.
Um resumo não substitui o arquivo nem prova que um teste continua válido após
outra mudança. Na retomada, confira os arquivos-alvo antes de editar.

## Separar tarefas por responsabilidade

Conteúdo, layout, runtime e validação têm skills próprias. Não é necessário
delegar ou iniciar subagentes; o mesmo agente pode seguir cada skill em sequência.
Modelos fechados podem receber um context pack e um único fragmento sem conhecer
o restante do projeto. O build local incorpora todo o motor no HTML entregue.

## Falhas típicas a evitar

- Ler milhares de linhas antes de identificar o slide.
- Gerar uma aula sem brief/objetivos.
- Reescrever ZIP/PPTX só porque não carregou o módulo existente.
- Editar apenas o compilado e perder a alteração no próximo build.
- Economizar contexto criando `<script src="tools/...">` na apresentação final.
- Dizer "testado" por copiar uma conclusão antiga de outro agente.
