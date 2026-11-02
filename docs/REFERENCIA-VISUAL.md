# Forma — referência visual e decisões do catálogo

Nota de evolução: este documento descreve a origem do catálogo. A identidade
atual é Signal Light, aprovada e aplicada aos dois presets; veja [SIGNAL-LIGHT](SIGNAL-LIGHT.md).

Abra **[`template-aulas.html`](../template-aulas.html)** no navegador. O arquivo contém os estilos, os 21 exemplos, as orientações para agentes e o exportador PPTX. Funciona localmente, inclusive sem internet e sem instalar pacotes.

Este documento consolida o desenho original do catálogo. O fluxo atual de fontes e build está em [README](../README.md); os comandos canônicos estão em [COMMANDS](COMMANDS.md). Para desenvolvimento modular, edite os fragmentos de um projeto e recompile, em vez de editar somente o HTML final.

## Direção visual e avaliação do modelo original

O template parte da linguagem de `aula-v2.html`: títulos fortes, checklists, contrastes claros/escuros, painéis laterais, blocos categorizados e diagramas. A nova proposta organiza esses recursos em um sistema reutilizável.

| Recurso do modelo de referência | Proposta no novo template |
|---|---|
| Circuitos e marca como imagens de fundo | Identidade geométrica em formas e rodapé textual personalizável |
| Títulos e faixas de seção | Hierarquia de seção, título e subtítulo; divisória escura para mudança de unidade |
| Checklists de apresentação pessoal | Lista com ícones reais, credencial e detalhe alinhados |
| Caixas escuras e avisos | Painéis claros, suaves ou escuros; chamadas de atenção consistentes |
| Colunas e listas densas | Grades de 2, 3 ou 4 colunas com espaçamento e extensão de texto controlados |
| Fluxo do ciclo de vida | Processo com etapas conectadas e entregas visíveis |
| Triângulos e árvores | Tríade vetorial e diagrama com nós e conectores editáveis |
| Tabelas e escalas de risco | Matriz de critérios, rubrica e etiquetas com contraste legível |
| Navegação inferior | Barra superior direita com navegação, seleção, notas, impressão, apresentação e PPTX |

**Novos recursos didáticos:** objetivos observáveis, linha do tempo, dados com interpretação, caso guiado, código com destaque de sintaxe, atividade com tempo e entrega, checagem de compreensão, síntese e próximo passo.

A identidade usa branco levemente quente, azul-petróleo, verde-teal e âmbar. O contraste é reforçado por rótulos e texto, sem depender só de cor. Arial e fontes locais mantêm o documento independente de fontes web.

## Usar e personalizar

1. Faça uma cópia do HTML com o nome da nova aula.
2. Configure `data-brand`, `data-course` e `data-author` em `#deck`.
3. Edite também `<title>`, os textos da capa e a apresentação do docente.
4. Escolha os layouts úteis; duplique, remova e reordene as seções `.slide`.
5. Troque textos, links, rótulos e notas pelos conteúdos reais da aula.
6. Ajuste as variáveis em `:root` para personalizar a identidade.

A numeração, o seletor de slides e os rodapés são construídos automaticamente ao abrir o arquivo. Recarregue o HTML depois de modificar sua estrutura.

### Catálogo de layouts

| Nº | `data-layout` | Conteúdo e variações |
|---|---|---|
| 01 | `capa` | Abertura de aula, curso ou workshop; título e promessa de aprendizagem |
| 02 | `docente` | Facilitador, convidado ou equipe; credenciais, abordagem e contato |
| 03 | `objetivos` | Resultados observáveis, competências ou critérios de sucesso |
| 04 | `roteiro` | Agenda, plano de módulo, tempos e combinados de avaliação |
| 05 | `divisoria` | Mudança de capítulo, início de unidade ou transição para prática |
| 06 | `conceito` | Definição com contexto, princípio, padrão ou legislação |
| 07 | `comparacao` | Duas alternativas, antes/depois ou prós/contras com critérios simétricos |
| 08 | `categorias` | Princípios, tipos, requisitos e classificações em 3–6 cards |
| 09 | `processo` | Método, procedimento, ciclo de vida ou sequência de execução |
| 10 | `timeline` | Marcos históricos, cronograma ou trilha de estudo |
| 11 | `diagrama` | Arquitetura, relações, árvore ou fluxo de dados |
| 12 | `triade` | Três perspectivas interdependentes, pilares ou restrições |
| 13 | `tabela` | Matriz de critérios, rubrica, responsabilidades ou riscos/controles |
| 14 | `dados` | Comparações quantitativas com escala, fonte e interpretação |
| 15 | `exemplo` | Caso guiado, exercício resolvido ou decisão comentada |
| 16 | `codigo` | Trecho de código, pseudocódigo, fórmula ou raciocínio técnico |
| 17 | `atividade` | Instruções, tempo, entrega e critérios para prática |
| 18 | `checagem` | Enquete, diagnóstico, questão conceitual ou exit ticket |
| 19 | `sintese` | Revisão das ideias-chave e transferência para outro contexto |
| 20 | `referencias` | Fontes utilizadas e leituras obrigatórias/complementares |
| 21 | `encerramento` | Dúvidas, compromisso de aplicação e próximo encontro |

Os textos são exemplos para orientar a composição; não constituem uma aula pronta sobre uma disciplina específica. Os dados do gráfico são fictícios. Os links de referências exemplificam repositórios e devem ser substituídos pelas fontes utilizadas.

## Orientações para agentes de IA

O próprio HTML contém:

- um guia geral no início do arquivo;
- um comentário `GUIA` antes de cada layout, com conteúdo recomendado e variações;
- um atributo `data-layout` estável para identificar os modelos;
- uma seção `<aside class="speaker-notes">` por slide.

Use os comentários como instruções de geração e as notas como orientação de apresentação. As notas não aparecem no slide, na impressão ou no modo apresentação. Elas são incluídas no campo de notas do apresentador no PPTX.

**Roteiro sugerido:** capa → objetivos → roteiro → conceitos → exemplos → prática → checagem → síntese → referências. Insira divisórias entre unidades.

Prefira uma ideia por slide, 3–5 itens por lista e poucos parágrafos. Quando o conteúdo não couber, divida o slide; não comprima toda a tipografia. Preserve espaço para título e rodapé.

## Controles

Todos os controles ficam no **canto superior direito**:

- **← / →:** slide anterior ou seguinte;
- **seletor:** navegação direta pelo título do slide;
- **Notas:** painel privado de preparação;
- **Imprimir:** todos os slides, um por página em 16:9;
- **Apresentar:** tela cheia, ocultando a interface;
- **Exportar PPTX:** geração e download inteiramente no navegador.

Atalhos: `←`, `→`, `PageUp`, `PageDown`, `Espaço`, `Home`, `End`, `F` e `Esc`. Em dispositivos de toque, deslize horizontalmente.

No modo apresentação, mova o ponteiro até a faixa superior para revelar os controles. `Esc` sai da tela cheia ou do modo apresentação em janela, caso o navegador não disponibilize tela cheia.

## Impressão 16:9

A prancheta é fixa em **1280 × 720**. O CSS de impressão define uma página de **13⅓ × 7½ polegadas**, equivalente a 960 × 540 pontos, sem margens. Cada slide gera uma página e a interface é ocultada.

O arquivo imprime todos os slides, independentemente do slide ativo. Para PDF, use **Salvar como PDF**, sem cabeçalhos/rodapés e preservando o tamanho definido pelo CSS. Uma impressora física com papel diferente pode aplicar margens ou escala próprias; a página gerada pelo template permanece 16:9.

## Como funciona a exportação PPTX

O exportador está **dentro do HTML** e usa apenas APIs nativas de JavaScript:

1. Clona cada slide em uma área de medição a 1280 × 720, fora da tela.
2. Lê dimensões e estilos calculados depois que grid, flex e quebras de texto foram resolvidos.
3. Converte preenchimentos, bordas, cantos, polígonos e linhas em formas DrawingML.
4. Usa `Range` para medir as linhas de texto e preservar posição, negrito, itálico, cor e links.
5. Gera partes OOXML de apresentação, slides, tema, mestre, layout e notas.
6. Monta um ZIP com CRC32 e diretório central próprios e entrega o `.pptx` como `Blob`.

**Não há screenshots, rasterização, imagens de fundo, base64 de imagens, bibliotecas, CDN ou chamadas a serviços.**

### Editabilidade

Todos os objetos visuais do catálogo são formas, conectores ou caixas de texto editáveis. Isso inclui o desenho da capa, os checks, a tríade, as barras e as células da matriz.

- Cada linha visual é uma caixa de texto, com trechos formatados dentro dela. Isso preserva as quebras do navegador. Para grandes reescritas no PowerPoint, reorganize ou una as caixas.
- Tabelas são conjuntos de células e textos editáveis, **não** tabelas nativas do Office.
- Gráficos são conjuntos de barras, rótulos e valores editáveis, **não** gráficos com planilha vinculada.
- O arquivo usa fontes locais. Ter as mesmas fontes instaladas no computador de destino ajuda a preservar a aparência. A renderização de fontes pode variar entre PowerPoint, LibreOffice e navegador.

### Contrato para novos elementos

| Recurso HTML/CSS | Saída no PPTX |
|---|---|
| Fundo de cor sólida | Forma com preenchimento e transparência |
| Borda sólida uniforme | Contorno editável |
| Bordas diferentes por lado | Linhas individuais editáveis |
| `border-radius` | Geometria vetorial com curvas |
| `clip-path: polygon(...)` | Forma livre editável |
| Texto HTML, `strong`, `em`, `span`, `br`, `pre` | Caixas de texto com trechos formatados |
| Links HTTP(S), `mailto:` e âncoras de slides | Hiperlinks do PowerPoint |
| `.connector[data-shape="line"]` | Linha ou conector com seta opcional |
| `data-shape` | `rect`, `roundRect`, `ellipse`, `triangle`, `diamond`, `chevron`, `rightArrow` ou `line` |

Use pares simples de valores `%` ou `px` em polígonos. Para conectores, mantenha as coordenadas `data-x1`, `data-y1`, `data-x2`, `data-y2` relativas à sua caixa e atualize o desenho HTML equivalente. `data-arrow="end"` acrescenta uma seta no PPTX. Conectores devem vir antes dos nós no DOM para ficar atrás deles.

O validador interrompe a exportação ao encontrar, por exemplo, imagens, canvas, SVG genérico, gradientes, sombras, filtros, transformações no conteúdo ou elementos que ultrapassem a prancheta. Isso evita exportar silenciosamente uma imagem ou descartar um recurso incompatível. O pequeno SVG usado nos exemplos de conectores é interpretado pela geometria `data-shape="line"`; ele não é incorporado como imagem.

Para conteúdo visual novo, prefira os componentes existentes e elementos HTML reais. Use ordem DOM para sobreposição, sem `z-index`, e evite conteúdo em pseudo-elementos.

### API pública

```javascript
// Diagnósticos sobre os slides atuais; [] significa que o contrato foi atendido.
const problemas = await AulaTemplate.validate();

// Download nativo.
await AulaTemplate.exportPptx();

// Arquivo binário para integração, sem disparar download.
const bytes = await AulaTemplate.exportPptx({ download: false });

// Navegação começa em 1.
AulaTemplate.goTo(3);
console.log(AulaTemplate.current, AulaTemplate.slideCount);
```

## Verificação realizada

Execute:

```bash
python3 tools/validate.py --strict
```

Execute a partir da pasta `presentation-template/`. O script usa a biblioteca padrão do Python e o Brave/Chromium instalado. No modo `--strict`, exige LibreOffice e `pdfinfo` para abertura/renderização e conferência das páginas. **Esses programas são ferramentas de teste; o HTML não depende deles.**

Verificações:

- navegação, seletor via API, atalhos e notas;
- exportação de texto alterado no DOM, confirmando que o deck não é fixo no exportador;
- ausência de problemas nos 21 layouts e rejeição de elemento incompatível;
- integridade ZIP, XML e relacionamentos internos;
- tamanho 16:9, textos editáveis e ausência de imagens no PPTX;
- notas de todos os slides e links das referências;
- PDF de impressão com 21 páginas, sem página extra;
- abertura e renderização do PPTX no LibreOffice.

Artefatos atuais ficam em `artifacts/validation/` (ou no caminho passado em `--out`). A comparação visual inicial entre o HTML impresso e o PPTX renderizado foi feita para os 21 layouts. A validação de abertura foi no LibreOffice, não no Microsoft PowerPoint. Consulte [TESTING](TESTING.md) para distinguir o PPTX de integração do export original.
