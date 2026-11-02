# Histórico de avaliação visual — Signal Light aprovado

**Versão aprovada: [tech-v2.html — Signal Light](tech-v2.html)**. A V1 recebeu o
feedback “escura demais”. A V2 mantém a linguagem tecnológica e usa fundos claros
na capa, arquitetura, indicadores e interface. Grafite fica nos textos e em um
pequeno núcleo do desenho; azul, ciano e lima permanecem como detalhes.

Para comparação, abra **[tech-v1.html](tech-v1.html)**. São cinco slides autocontidos
para avaliar a direção **Signal**: grafite, azul elétrico, ciano e lima,
microrrótulos monoespaçados, divisórias técnicas e geometria vetorial.

- O usuário aprovou a V2 com “Ficou boa.”; a promoção aos dois presets está concluída.
- Os experimentos ficam em `tech-v1/theme-preview.css` e `tech-v2/theme-preview.css`.
  A V2 embute a base V1 e suas alterações de cores no próprio HTML, sem dependência externa.
- A identidade de produção fica em `tools/styles/signal-light.css`, sem dependência de previews/.
- A exportação PPTX, impressão e controles são os mesmos do produto.
- Os catálogos geral e educacional já usam o tema claro aprovado.

```bash
python3 tools/run.py build --project previews/tech-v2/project.json
python3 tools/run.py validate previews/tech-v2.html --out artifacts/tech-v2 --strict
```

Os HTMLs de prévia preservam o contexto da avaliação (inclusive rótulos de
“aguardando aprovação”). Para uso atual, abra os catálogos na raiz da solução.
Novas direções visuais devem passar por uma nova avaliação antes da promoção.
