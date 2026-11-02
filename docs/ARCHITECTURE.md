# Arquitetura e mapa de arquivos

`presentation-template/` é a raiz independente. `common.ROOT` é calculado a partir de tools/,
nunca pelo experimento pai. O preset geral está em `src/general/`; o educacional
é opcional em `src/`. O estilo em previews/ não é dependência dos presets.
O bundle incorpora estrutura (`theme.css`), identidade aprovada (`signal-light.css`)
e impressão (`print.css`) nessa ordem. A arte compartilhada em
`src/components/signal-board.html` é expandida nos marcadores dos fragmentos;
nenhum include permanece no HTML final.

`prepare.py` compila ferramentas para `.cache/python/`, nível 1; `run.py` executa
os CLIs com esse prefixo. A distribuição não leva bytecode: `prepare.py --clean`.

## Dois ambientes, um contrato

**Desenvolvimento:** Python lê shell, fragmentos, CSS e JS separados.
**Distribuição:** um único HTML com tudo embutido; só o navegador é necessário.

```text
project.json + slides/*.html + CSS local
                 +
src/shell.html + tools/bundle.json + tools/styles + tools/runtime
                 ↓ tools/build.py
             apresentacao.html
                 ├─ navegador → projeção / notas / navegação
                 ├─ window.print + @page → PDF 16:9
                 └─ DOM → DrawingML → OOXML → ZIP → PPTX editável
```

## Ordem dos scripts embutidos

| Arquivo em tools/runtime | Responsabilidade |
|---|---|
| `viewer.js` | Metadados/rodapés, notas, navegação, escala e atalhos |
| `presentation.js` | Fullscreen, fallback e controles na projeção |
| `print.js` | Ação de impressão |
| `zip.js` | `FormaZip`: ZIP STORE, CRC32, diretório central |
| `pptx-drawing.js` | `FormaDrawing`: XML, EMU, formas, curvas, texto/runs e links |
| `pptx-dom.js` | `FormaDOM`: inspeção, clone isolado, medição e percurso DOM |
| `pptx-package.js` | `FormaPackage`: slides, layouts, mestres, tema e notas |
| `export-pptx.js` | `Pptx`: geração/download e mensagens |
| `bootstrap.js` | API pública `AulaTemplate` e botão de exportação |

`FormaPresentation` é o nome agnóstico da mesma API; `AulaTemplate` permanece alias.

Cada módulo encapsula helpers em uma IIFE. O build concatena os scripts em um
único bloco clássico, na ordem de `bundle.json`; sem imports e sem carregamento
externo. Funções de navegação/apresentação compartilham o estado do viewer.

## Caminho do exportador

1. Espera `document.fonts.ready`.
2. Clona um slide de cada vez em `.export-host`, fixo em 1280×720.
3. Recusa conteúdo fora do contrato antes da conversão.
4. Percorre a ordem DOM: fundo/bordas, geometria, descendentes e textos.
5. `Range` mede caracteres e agrupa runs em linhas; estilos são calculados.
6. Gera XML OOXML, relationships e content types.
7. ZIP nativo produz `Uint8Array`; `Blob`/URL temporária dispara o download.
8. Remove o clone em `finally` e preserva o slide ativo.

## Testes não são runtime

`browser/audit.js` é injetado numa cópia temporária do HTML pelo `common.py`.
Ele executa a API real e retorna JSON pelo DOM. Não há flags de debug permanentes
no artefato final. Os modos são `validate`, `integration` e `export`.

- `integration`: muda um título para provar que o conteúdo não é hardcoded.
- `export`: não muda conteúdo; é usado para o arquivo original.
- `validate`: somente verifica contrato/layout.

`validate_pptx.py` verifica estrutura; `render_office.py` verifica abertura/render.
`print_pdf.py` examina todas as páginas com `pdfinfo` quando disponível.

## Locais para mudanças

Texto de uma aula → fragmento do projeto. Identidade da aula → CSS local.
Componente reutilizável → `theme.css`. Impressão → `print.css`/`print.js`.
Nova forma → DrawingML + inspeção DOM + exemplo + teste + contrato.
Arquivo PPTX reparado na abertura → package/relationships + validador OOXML.
