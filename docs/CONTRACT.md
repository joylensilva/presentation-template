# Contrato de HTML, PPTX e autocontenção

## Obrigatório no entregável

- Um único `.html`, UTF-8, com CSS e scripts internos.
- Prancheta fixa 1280×720 e escala uniforme em tela.
- Navegação, apresentação, impressão e exportação PPTX dentro do arquivo.
- Texto real e formas editáveis. Nenhum screenshot como representação de slide.
- Uma seção de notas por slide, privada na tela/impressão.

Fontes de desenvolvimento podem ser separadas; devem ser embutidas no build.
O marcador `<!-- FORMA:SIGNAL_ART -->` também é exclusivamente de desenvolvimento:
o build expande a arte em elementos reais, e o check recusa marcadores não resolvidos.
Links HTTP(S)/mailto de conteúdo são permitidos. Recursos de execução externos,
mesmo locais (`tools/x.js`, `tema.css`), não são permitidos.

## Componentes preferidos

`.slide-header`, `.content`, `.stack`, `.row`, `.grid`, `.cols-2/3/4`, `.split`,
`.panel`, `.tint`, `.dark`, `.badge`, `.callout`, `.list`, `.bullet`, `.check`,
`.number`, `.rule`, `.table`, `.chart`, `.diagram`, `.connector`, `.triangle`.
Os layouts de `src/slides/` mostram a marcação correta de cada composição.

## Suporte no PPTX

| HTML/CSS | Representação |
|---|---|
| Fundo sólido e alpha | Forma com preenchimento |
| Bordas sólidas iguais/diferentes | Contorno / linhas individuais |
| `border-radius` | Forma vetorial com curvas |
| `clip-path:polygon` com pares simples `%`/`px` | Forma livre |
| Texto, strong/em/span, br/pre | Texto por linha com runs de estilo |
| Links http(s), mailto e #slide | Hiperlinks |
| `data-shape="line"` + coordenadas | Linha/conector e seta opcional |
| Grid/flex/posicionamento | Dimensões medidas no navegador |

Presets `data-shape`: rect, roundRect, ellipse, triangle, diamond, chevron,
rightArrow, line. Mantenha a representação CSS/HTML equivalente para o navegador.
SVG genérico não é convertido. O SVG simples dos conectores é interpretado
pelos atributos `data-shape`, `data-x1/y1/x2/y2`, e não incorporado como imagem.

## Evitar em conteúdo de slides

Imagens/canvas/vídeo/iframe, background url/base64, gradientes, sombras,
filtros, transformações/rotações, `z-index`, fontes web, pseudo-elementos
decorativos e listas com marcadores que não existem como elementos reais.
Use elementos DOM em vez de `::before/::after` e ordem DOM para sobreposição.
Não aplique variações tipográficas complexas (texto vertical, CSS masks etc.)
fora dos componentes sem ampliar o suporte e os testes.

## Precisão de editabilidade

Cada linha visual é uma caixa de texto; negrito/itálico/cor/links são runs nela.
Uma reescrita extensa pode exigir unir/reorganizar caixas. Células de tabela
e barras de gráfico são formas/textos individuais, não objetos nativos Office
com planilha. Conectores não prometem vínculo dinâmico aos nós após movê-los.

O mapeamento conserva a geometria medida, mas fontes/motores podem renderizar
com pequenas diferenças. Abertura no LibreOffice não equivale a teste no PowerPoint.

## Medidas e limites

- 1 CSS px = 9525 EMU; slide = 12192000×6858000 EMU.
- 24px CSS = 18pt no PPTX; OOXML usa 1800 em centésimos de ponto.
- PDF de impressão = 960×540 pt; margens zero.
- O exportador não interpreta todo CSS possível. Use o catálogo e valide.
- `self_contained.py` é uma verificação conservadora de estrutura/recursos,
  não uma prova formal da semântica de JavaScript arbitrário.

## Extensão responsável

Para um elemento novo, registre spec e exemplo mínimo, defina equivalência
editável, acrescente diagnóstico e teste, recompile e compare visualmente.
Não contorne o validador com imagens ou ocultando o problema na exportação.
