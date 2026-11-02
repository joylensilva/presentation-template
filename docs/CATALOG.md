# Catálogo completo de exemplos

A raiz da solução é **presentation-template/**. O preset geral tem **21 exemplos**,
preservando todos os tipos do educacional sem restringi-los a aulas. Ambos usam
Signal Light e o mesmo motor autocontido de PPTX, impressão e apresentação.

## Equivalências e variações

| Nº | Layout geral | Tipo preservado / usos possíveis |
|---|---|---|
| 01 | `capa` | Abertura, promessa, proposta, evento |
| 02 | `apresentador` | Docente → apresentador, equipe, liderança, consultoria |
| 03 | `objetivos` | Direção, resultados, decisões ou competências |
| 04 | `roteiro` | Agenda, alinhamentos, reunião ou workshop |
| 05 | `divisoria` | Transição de capítulo, tema ou fase |
| 06 | `conceito` | Conceito, contexto, diagnóstico ou oportunidade |
| 07 | `comparacao` | Alternativas, soluções, antes/depois |
| 08 | `categorias` | Cards de dimensões, princípios, capacidades |
| 09 | `processo` | Fluxo de etapas, método, execução |
| 10 | `timeline` | Marcos, história, roadmap, cronograma |
| 11 | `diagrama` | Arquitetura, conexões, relações |
| 12 | `triade` | Três pilares ou restrições interdependentes |
| 13 | `tabela` | Matriz de critérios, responsabilidades, rubrica |
| 14 | `dados` | Indicadores, gráfico de barras e interpretação |
| 15 | `exemplo` | Caso guiado, problema resolvido, decisão comentada |
| 16 | `codigo` | Código, pseudocódigo, fórmula ou demonstração |
| 17 | `atividade` | Dinâmica, plano de trabalho, colaboração ou prática |
| 18 | `checagem` | Enquete, alinhamento, pergunta ou checagem de compreensão |
| 19 | `sintese` | Síntese executiva, conclusão ou recomendação |
| 20 | `referencias` | Fontes, evidências, bibliografia e premissas |
| 21 | `encerramento` | Próximos passos, chamada para ação, contato |

Os números dos arquivos acompanham a ordem do manifesto. O catálogo é um
repertório de exemplos, não um roteiro obrigatório de 21 slides para cada projeto.
Use `--layouts` para selecionar apenas os modelos necessários ao brief.

## Proteção contra perda de exemplos

`tools/check_structure.py` e o teste
`test_general_preserves_every_educational_example_type` verificam que todos os
tipos educacionais têm equivalente no geral, sem duplicações. O domínio dos
textos pode mudar; a variedade de estruturas não deve ser reduzida por isso.

## Comandos — a partir da nova raiz

```bash
python3 tools/prepare.py
python3 tools/run.py inspect --catalog
python3 tools/run.py structure
python3 tools/run.py test
python3 tools/run.py build
python3 tools/run.py validate --out artifacts/catalog-restored --strict
```

`template-apresentacoes.html` é o entregável geral autocontido.
`template-aulas.html` mantém os 21 exemplos educacionais. O diretório experimental
pai não é necessário. Configurações, skills e ferramentas usam a nova raiz.

## Verificação da restauração

- 8 testes aprovados, incluindo regressão da cobertura dos tipos e portabilidade da raiz.
- Catálogo geral: 21 slides e 21 notas; nenhum diagnóstico de layout na auditoria.
- PPTX original: 640 formas, 415 caixas de texto, 38 conectores e zero imagens.
- Impressão HTML e renderização LibreOffice: 21 páginas de 960×540 pt em ambos.
- Os 21 exemplos foram inspecionados visualmente nas montagens HTML e PPTX/Office.
- Relatórios e arquivos: `artifacts/catalog-restored/`.

Relatórios anteriores em artifacts/ são históricos e podem mencionar o nome
antigo da pasta e a versão de 10 slides. Não são dependências nem evidências
da versão corrente. O checkpoint atual é `SESSION.json` nesta nova raiz.
