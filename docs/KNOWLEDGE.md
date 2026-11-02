# Conhecimento consolidado

## Da reprodução da aula ao template

O trabalho começou ajustando `aula-v2.html` às referências PNG, incluindo
tipografia, diagramas e alinhamento de checkboxes. O sistema reutilizável mantém
as propostas de checklists, painéis, comparações, fluxos e tríades, com identidade
geométrica moderna e novos layouts didáticos.

Referências visuais não devem ser substituídas por suposições extraídas de um
gerador antigo. Confira texto e aparência na fonte definida pelo usuário.

## Lições de layout

- Alinhe checkbox e bloco de texto pelo flex/grid; centralize o check dentro
  da caixa. Caixa e glyph são dois problemas de alinhamento diferentes.
- Uma imagem injetada por `content:url(...)` pode ter comportamento intrínseco
  surpreendente. No histórico, o QR foi corrigido usando `src` no `<img>`.
  O novo contrato usa geometria/texto reais e não inclui imagens no PPTX.
- A moldura cinza e o menu do navegador não fazem parte da prancheta. Compare
  a área 16:9 com a referência, ou use os PDFs de impressão.
- Use escala uniforme na tela; retire a escala na impressão/medição de exportação.
- Corrija conteúdo excessivo dividindo slides, não comprimindo a aula inteira.

## Lições do PPTX

- PPTX é um pacote ZIP de XML e relationships; fechar um ZIP não basta.
- Content types precisam cobrir partes existentes; todos os targets internos
  e r:ids devem resolver; IDs de forma não podem se repetir no slide.
- Medição fora da tela a 1280×720 evita herdar escala da interface.
- Range permite manter rich text e quebras sem rasterizar, em caixas por linha.
- As notas devem estar no OOXML de notesSlides, não visíveis na composição.
- Tabelas e gráficos do template são formas/textos editáveis, não objetos
  nativos Office com dados vinculados.
- Abertura no LibreOffice e comparação visual complementam a validação estrutural.

## Lições de testes

- O teste de conteúdo mutado precisa usar uma string curta que caiba em todos
  os layouts; uma string longa pode provocar overflow legítimo.
- Teste de integração tem arquivo claramente identificado; export de produção
  usa outro modo que não altera o DOM da aula.
- Fullscreen sem gesto confiável pode travar/não resolver em headless. Teste
  o fallback explicitamente e reserve o fullscreen real à verificação manual.
- Contagem de páginas deve ser dinâmica para aulas novas e examinada em todas
  as páginas, não só na primeira.
- Não reutilize uma saída antiga para comprovar que um comando novo funcionou.
- Dependências de teste e fontes modulares não podem vazar para o HTML final.

## Limites e honestidade

Não há promessa de converter qualquer HTML arbitrário. Não há teste automático
no Microsoft PowerPoint neste ambiente. Não há garantia baseada só em quantidade
de parâmetros de modelos locais. O suporte real é o contrato documentado,
os layouts testados e as evidências registradas.
