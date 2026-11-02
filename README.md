# Forma — raiz independente para apresentações

**Abra [`template-apresentacoes.html`](template-apresentacoes.html)** para o preset
geral de 21 layouts. O preset educacional de 21 layouts continua disponível em
[`template-aulas.html`](template-aulas.html). Cada HTML funciona sozinho.

Esta pasta **presentation-template/** é a raiz da solução: abra o projeto e execute os agentes
aqui. Pode copiá-la para outro local sem levar a pasta experimental, o HTML
original ou seus testes antigos. Todos os caminhos do produto partem desta raiz.

**Visual aprovado e aplicado:** Signal Light, com fundos claros, grafite,
azul elétrico e detalhes ciano/lima. Os dois catálogos já usam essa identidade.
As [prévias](previews/README.md) ficam como histórico; a fonte canônica é
`tools/styles/signal-light.css` e não depende delas.

Para agentes: comece por **[`AGENTS.md`](AGENTS.md)**. Para requisitos e critérios
de aceite: **[`SDD.md`](SDD.md)**.

## Desenvolvimento modular; entrega autocontida

Os códigos são separados para facilitar manutenção e uso por modelos com contexto
limitado. O build **embute** os estilos e scripts no HTML final; não cria links
para os arquivos de `tools/`. O HTML entregue já inclui exportador PPTX nativo,
impressão 16:9, navegação, notas e modo apresentação.

```text
presentation-template/
├── template-apresentacoes.html  # preset geral padrão, autocontido
├── template-aulas.html          # preset educacional anterior
├── AGENTS.md / SDD.md           # entrada dos agentes e requisitos
├── README.md / opencode.json
├── src/
│   ├── shell.html              # estrutura da aplicação e guia embutido
│   ├── general/                # preset geral, manifesto e fragmentos
│   ├── project.json            # manifesto educacional opcional
│   ├── catalog.json            # índice educacional
│   └── slides/                 # layouts educacionais
├── tools/
│   ├── build.py                # compilação determinística para um HTML
│   ├── prepare.py / run.py      # preparação local e executor otimizado
│   ├── new_presentation.py     # novo projeto geral ou educacional
│   ├── context_pack.py         # contexto curto por tarefa/slide
│   ├── inspect_slides.py       # catálogo, resumo ou um fragmento
│   ├── self_contained.py       # verificação estática do entregável
│   ├── validate.py             # pipeline integrado
│   ├── export_pptx.py          # executa o JS do HTML, sem mutar conteúdo
│   ├── validate_pptx.py        # ZIP, XML, rels e objetos editáveis
│   ├── print_pdf.py / render_office.py
│   ├── screenshot.py / contact_sheet.py / doctor.py
│   ├── runtime/               # JS nativo separado por responsabilidade
│   ├── styles/                # estrutura, Signal Light e impressão
│   ├── browser/               # harness exclusivo de testes
│   ├── tests/                 # regressões do tooling
│   └── skills/                # seis skills canônicas
├── tasks/                     # brief, storyboard, spec, sessão e revisão
├── docs/                      # comandos, arquitetura, contrato e conhecimento
├── prompts/                   # instruções curtas para agentes
├── .opencode/commands/        # atalhos opcionais para OpenCode
├── previews/                  # histórico da avaliação visual aprovada
├── projects/                  # fontes de novas apresentações
└── artifacts/                 # relatórios e arquivos de teste
```

## Fluxo rápido

Todos os comandos desta documentação partem da pasta `presentation-template/`.

```bash
python3 tools/prepare.py
python3 tools/run.py doctor
python3 tools/run.py new --directory projects/proposta-01 --title "Proposta de projeto"
```

Preencha `BRIEF.md`, `STORYBOARD.md`, metadados de `project.json` e os fragmentos
em `projects/proposta-01/slides/`. Os textos iniciais são demonstrativos.

```bash
python3 tools/run.py build --project projects/proposta-01/project.json
python3 tools/run.py standalone projects/proposta-01/apresentacao.html
python3 tools/run.py validate projects/proposta-01/apresentacao.html --out artifacts/proposta-01 --strict
```

Distribua **`projects/proposta-01/apresentacao.html`**. Basta esse arquivo.

Para aulas, acrescente `--preset education` ao comando `new`. O campo `course`
do manifesto continua por compatibilidade: em apresentações gerais, significa
tema/linha de rodapé; `author` identifica o apresentador e `brand`, a organização.

### Manter o catálogo

```bash
python3 tools/run.py build
python3 tools/run.py build --check
python3 tools/run.py structure
python3 tools/run.py test
python3 tools/run.py validate --strict
```

### Exportar arquivos originais

```bash
python3 tools/run.py export --output artifacts/catalogo-original.pptx
python3 tools/run.py print --output artifacts/catalogo-original.pdf --strict
```

Esses comandos usam o catálogo geral por padrão; passe o caminho do HTML para
exportar uma apresentação específica.

## Recursos do HTML

- Layouts para contexto, estratégia, alternativas, dados, arquitetura e próximos passos.
- Preset educacional opcional para objetivos, conceitos, prática e revisão.
- Comentários GUIA por layout e notas do apresentador exportadas ao PPTX.
- Controles no canto superior direito; atalhos e gestos de navegação.
- Projeção em tela cheia, com alternativa em janela quando a API é recusada.
- Impressão de todos os slides em páginas 16:9, sem notas ou controles.
- PPTX sem bibliotecas externas, com textos, formas e conectores editáveis.

**Precisão sobre editabilidade:** linhas de texto são caixas editáveis; tabelas
são células/formas; gráficos são barras e rótulos. Não há planilhas vinculadas,
tabelas nativas ou screenshots. Veja [`docs/CONTRACT.md`](docs/CONTRACT.md).

## Ferramentas necessárias

Para abrir o HTML: navegador moderno. Para build e ferramentas: Python 3.10+.
Para testes no navegador: Brave/Chromium (`FORMA_BROWSER` pode indicar o executável).
Para validação completa: LibreOffice e `pdfinfo`. Para índices visuais: `pdftoppm`.
Sem Node, npm, pip ou serviços obrigatórios. As dependências de teste não são
dependências do entregável.

## Primeira rodada e bytecode local

Execute `python3 tools/prepare.py` no início. O script verifica a sintaxe e prepara
bytecode com otimização nível 1 em `.cache/python/`; o executor `run.py` reutiliza
esse cache e revalida as fontes quando elas mudam. Isso reduz trabalho de parsing
nas importações; não é uma promessa de acelerar os algoritmos de exportação.

O cache depende da instalação/Python e **não acompanha a solução distribuída**.
Não há necessidade de `tools/__pycache__`. Para entregar/copiar uma raiz limpa:

```bash
python3 tools/prepare.py --clean
```

O próximo agente fará a preparação novamente. Scripts diretos permanecem
compatíveis, mas `run.py` é o fluxo recomendado para reutilizar o bytecode otimizado.

## Agentes e contexto limitado

- [`tools/skills/`](tools/skills/) contém as skills; a tabela de rotas está em `AGENTS.md`.
- [`docs/CONTEXT.md`](docs/CONTEXT.md) orienta modelos 12B/27B sem prometer capacidade
  medida por tamanho de modelo.
- [`prompts/`](prompts/) tem instruções curtas para iniciar, retomar e revisar.
- No OpenCode, inicie a sessão nesta pasta para carregar `opencode.json`, skills
  e os comandos `/forma-create` e `/forma-validate`. Se já estava aberto, encerre
  e reinicie para carregar a nova configuração.
- Outros agentes podem ler `AGENTS.md` e os mesmos `SKILL.md` diretamente.

Mais detalhes: [comandos](docs/COMMANDS.md), [arquitetura](docs/ARCHITECTURE.md),
[testes](docs/TESTING.md), [problemas conhecidos](docs/TROUBLESHOOTING.md),
[lições acumuladas](docs/KNOWLEDGE.md) e [registro de validação](docs/VALIDATION.md).

Estado atual da raiz e da prévia: [ROOT-AND-PREVIEW](docs/ROOT-AND-PREVIEW.md).

Aplicação e validação do tema aprovado: [SIGNAL-LIGHT](docs/SIGNAL-LIGHT.md).

Catálogo completo e equivalências dos 21 exemplos: [CATALOG](docs/CATALOG.md).
