# Raiz independente, presets gerais e aprovação visual

## Decisão de estrutura

O nome atual confirmado pelo usuário é **presentation-template/**. Essa pasta é a raiz
do workspace, das configurações e dos novos projetos. O diretório experimental
pai é apenas histórico. A instalação pode ser movida sem código ou contexto do pai.

## Padrão agnóstico

- `general`: 21 layouts para apresentações executivas, técnicas, propostas, pitchs e eventos.
- `education`: os 21 layouts educacionais existentes, como opção explícita.
- Padrão de build/validação: `src/general/project.json` / `template-apresentacoes.html`.
- Compatibilidade: `course` é a linha de tema do rodapé; `AulaTemplate` continua
  alias de `FormaPresentation`. O exportador e seu contrato são compartilhados.
- Os textos são exemplos; o brief define conteúdo e domínio reais.

## Python na primeira rodada

`python3 tools/prepare.py` prepara/revalida bytecode de otimização nível 1 em
`.cache/python/`. `python3 tools/run.py` reutiliza esse bytecode. O cache é local,
ignorado e descartável; não é parte da solução distribuída. Bytecode pode evitar
parsing repetido de imports, mas não representa uma otimização dos algoritmos.

`python3 tools/prepare.py --clean` remove caches antes da distribuição. Nenhum
`tools/__pycache__`, `.pyc` ou cache pré-compilado deve acompanhar a entrega.

## Avaliação visual e proposta

O tema anterior é legível e consistente, mas usa cards arredondados e uma
hierarquia visual pouco distintiva. A proposta **Signal** testa:

- grafite em abertura/arquitetura, com páginas claras para dados;
- azul elétrico, ciano e lima como acentos funcionais;
- títulos mais editoriais e microrrótulos monoespaçados;
- cantos mais contidos, linhas finas e composição técnica;
- geometria vetorial real, sem imagens, gradientes ou efeitos raster.

Prévia atual: `previews/tech-v2.html` (Signal Light), com cinco slides. O usuário
gostou parcialmente da V1, mas a considerou escura demais. A V2 adota fundos
claros em toda a apresentação e interface, grafite no texto, azul elétrico nos
destaques e ciano/lima em detalhes. O único bloco grafite maior é o pequeno
núcleo do desenho da capa.

Fontes isoladas: `previews/tech-v2/theme-preview.css`, base V1 e manifesto próprio.
A V1 continua disponível para comparação; ambas são HTMLs autocontidos.

**Aprovação recebida:** o usuário confirmou a V2 com “Ficou boa.”. O tema foi
consolidado em `tools/styles/signal-light.css` e aplicado aos catálogos geral e
educacional. As prévias permanecem como histórico, não como dependências de produção.
A promoção também clareou divisórias, painéis de destaque, tabelas e código.
Veja `SIGNAL-LIGHT.md` para evidências da validação dos 31 layouts atualizados.

## Evidências desta rodada

Nota histórica: as contagens de 10 slides gerais abaixo correspondem à versão
anterior. A restauração para 21 exemplos e a renomeação estão em `CATALOG.md`.

- 7 testes passaram, incluindo cópia da raiz para um diretório independente,
  build sem o experimento, preparação do próprio bytecode e limpeza do cache.
- Preset geral: 10 slides, auditoria, PPTX editável, PDF 16:9 e abertura no LibreOffice.
- Prévia Signal: 5 slides, auditoria, PPTX editável, PDF 16:9 e abertura no LibreOffice.
- Revisão Signal Light V2: os mesmos checks passaram; capa, arquitetura e dados
  foram inspecionados nas capturas do navegador.
- Capa e slide de dados da prévia foram inspecionados em capturas do navegador.
- Relatórios: `artifacts/general-root-validation/report.json` e `artifacts/tech-v1/report.json`.
- Fullscreen com clique real e Microsoft PowerPoint não foram testados nesta rodada.

O registro em `VALIDATION.md` corresponde à versão educacional anterior; não
deve ser confundido com aprovação visual do Signal nem com resultados do preset geral.
