# Ferramentas — manutenção

Leia primeiro `../AGENTS.md` e a skill correspondente em `skills/`.

- Raiz: a pasta que contém este tools/, independentemente do caminho/nome do pai.
- Primeira rodada: `python3 tools/prepare.py`; comandos por `python3 tools/run.py`.
- Bytecode otimizado fica somente em `.cache/python/`, nunca em tools/__pycache__.
- Antes de distribuir a raiz: `python3 tools/prepare.py --clean`. Cache não é fonte.
- Não promova o estilo de previews/ sem aprovação explícita do usuário.

- Python: ferramentas de build/teste. Biblioteca padrão; sem pip/npm obrigatório.
- `runtime/*.js` e `styles/*.css`: fontes EMBUTIDAS no HTML pelo build.
- `browser/audit.js`: somente teste. Nunca inclua em `bundle.json`.
- Depois de alterar runtime/CSS: `python3 tools/build.py` na pasta `presentation-template/`.
- Nunca gere scripts externos no HTML para "economizar contexto".
- `common.py` resolve ferramentas e executa o navegador com timeout.
- Build determinístico: fontes iguais geram HTML igual; metadado `forma-build`
  contém hash das fontes. PPTX tem data de geração e não é binariamente determinístico.
- `validate.py --strict` exige navegador, LibreOffice e pdfinfo. Não o substitua
  por apenas testar ZIP/XML. São níveis de verificação distintos.
- Para mudar um mapeamento PPTX, leia apenas `runtime/pptx-drawing.js` ou
  `runtime/pptx-dom.js` inicialmente. Preserve API pública e contrato editável.
- Não fixe contagens de projetos: os dois presets têm 21 exemplos; projetos podem ter 1+.
- Preserve a cobertura dos tipos: generalizar não pode excluir exemplos do educacional.
