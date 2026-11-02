# Signal Light — tema aprovado e aplicado

Atualização do catálogo: ambos os presets agora têm **21 exemplos**, e a raiz
é `presentation-template/`. Veja [CATALOG](CATALOG.md). As estatísticas originais
de promoção do tema nesta página são históricas, anteriores à ampliação do geral.

O usuário aprovou a revisão clara com **“Ficou boa.”**. A identidade foi promovida
para os dois presets de produção; não há mais aprovação visual pendente.

## Fontes e entregáveis

- `tools/styles/theme.css`: estrutura e componentes-base.
- `tools/styles/signal-light.css`: identidade clara aprovada, sem dependência de previews/.
- `tools/styles/print.css`: preservação 16:9 na impressão.
- `src/components/signal-board.html`: arte vetorial compartilhada de capa/encerramento.
- `template-apresentacoes.html`: 21 layouts gerais atualizados.
- `template-aulas.html`: 21 layouts educacionais atualizados.

O marcador `<!-- FORMA:SIGNAL_ART -->` dos fragmentos é expandido pelo build.
O arquivo final contém todos os elementos reais e todos os scripts internos;
não precisa dos componentes, estilos, prévias ou ferramentas ao lado.

## Aplicação em todos os componentes

Fundos claros, textos em grafite, azul elétrico, ciano/lima pontuais, microrrótulos
monoespaçados, cantos discretos e rodapé técnico. Painéis de ênfase, divisórias,
tabelas e código também foram clareados. A classe `.panel.dark` permanece
compatível, mas sua aparência atual é um painel de ênfase azul-claro.

Formas de diagramas e tríades continuam vetoriais. A área grafite fica pontual
no pequeno núcleo da arte; não há slides inteiros escuros.

## Validação desta promoção

- 7 testes de regressão aprovados, incluindo build determinístico, recursos
  externos proibidos, criação dos dois presets e portabilidade da raiz/cache.
- Pipelines `--strict` aprovados para os 10 slides gerais e os 21 educacionais.
- Nenhum diagnóstico de overflow; notas, navegação, exportação e 16:9 verificados.
- PPTX original geral: 314 formas, 197 caixas de texto, 17 conectores, zero imagens.
- PPTX original educacional: 633 formas, 409 caixas de texto, 39 conectores, zero imagens.
- Ambos os PPTX originais abriram e renderizaram no LibreOffice.
- PDFs HTML e Office: respectivamente 10 e 21 páginas, todas 960×540 pt.
- Os 31 layouts foram revisados visualmente em montagens HTML e PPTX/Office.

Evidências regeneráveis em `artifacts/signal-light-general/` e
`artifacts/signal-light-education/`: `report.json`, `original-export.json`,
`original.pptx`, PDFs e índices visuais. O PPTX original é diferente do arquivo
de integração, que substitui deliberadamente um título para testar o exportador.

Microsoft PowerPoint e fullscreen com clique real não foram testados nesta rodada.
Após a validação, o bytecode de distribuição é limpo; o próximo agente começa
por `python3 tools/prepare.py`.

## Próximas mudanças

Use os estilos canônicos para manutenção. As prévias ficam como histórico;
uma identidade visual diferente deve ser apresentada e aprovada novamente.
