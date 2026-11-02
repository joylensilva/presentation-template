# SDD — Specification Driven Development

Versão: 1.1. Escopo: sistema Forma e apresentações gerais ou educacionais.
Este documento define o comportamento; não é uma implementação alternativa.

## 0. Raiz e aprovação visual

A pasta `presentation-template/` é a raiz independente dos projetos/agentes. Nenhuma ferramenta
ou configuração depende da pasta experimental pai. O preset padrão é `general`
(21 layouts); `education` preserva o uso educacional (21 layouts). Tema/organização/
apresentador são metadados gerais; nomes `course` e `AulaTemplate` ficam como
compatibilidade. A API agnóstica também está em `FormaPresentation`.

Primeira rodada: `tools/prepare.py` prepara bytecode otimizado nível 1 localmente;
`tools/run.py` reutiliza-o em `.cache/python/`. Não distribuir cache ou pyc.
`tools/prepare.py --clean` limpa esse estado antes de entregar uma cópia da raiz.
Bytecode reduz parsing/importação, sem prometer ganho dos algoritmos em si.

Signal Light (`previews/tech-v2.html`) foi aprovado explicitamente pelo usuário
com “Ficou boa.” e promovido a `tools/styles/signal-light.css`. A V1 foi descartada
por excesso de escuridão. Futuras mudanças de identidade continuam exigindo
aprovação explícita antes de alterar os temas compartilhados.

## 1. Objetivo e fluxo

Gerar apresentações visualmente consistentes para estratégia, propostas, pitchs,
conteúdo técnico, eventos e aulas, com um artefato HTML
autocontido e exportação nativa para objetos PowerPoint editáveis. Permitir
manutenção por agentes locais/remotos sem carregar todo o sistema no contexto.

Fluxo SDD:
1. **Brief:** registrar público, objetivo, duração, conteúdo e fontes.
2. **Spec:** definir a mudança e critérios de aceite em `CHANGE.spec.md`.
3. **Storyboard:** escolher uma ideia e um layout por slide.
4. **Implementação:** alterar as menores fontes necessárias.
5. **Verificação:** executar checks ligados aos requisitos afetados.
6. **Evidência:** registrar resultados e lacunas em `REVIEW.md`/`SESSION.json`.
7. **Entrega:** fornecer o HTML compilado e, se solicitados, os exports originais.

## 2. Invariantes do produto

| ID | Requisito verificável |
|---|---|
| R01 | O HTML final tem CSS e todo o JavaScript embutidos; nenhum asset externo é necessário para abrir/navegar/exportar/imprimir. |
| R02 | Prancheta 1280×720; proporção 16:9 por escala uniforme em tela e páginas 960×540 pt em impressão. |
| R03 | O exportador é JavaScript nativo; gera ZIP/OOXML sem bibliotecas, CDN, serviços ou screenshots. |
| R04 | Todos os elementos visuais suportados viram formas, conectores e texto editáveis; não há fallback raster. |
| R05 | Fonte/renderização sem suporte ou overflow relevante produz diagnóstico; não perde conteúdo silenciosamente. |
| R06 | Notas por slide ficam ocultas na projeção/impressão e são incluídas no campo de notas do PPTX. |
| R07 | Navegação, seletor, notas, impressão, apresentação e exportação ficam na barra superior direita. |
| R08 | Fullscreen e alternativa em janela preservam 16:9, navegação e saída com Esc. |
| R09 | Impressão inclui todos os slides, um por página, sem interface e sem página vazia final. |
| R10 | Quantidade de slides é variável (1+); não há conteúdo ou contagem de aula fixos no exportador/testes genéricos. |
| R11 | Fontes separadas e build determinístico; o bundle final não contém referências de execução a tools/. |
| R12 | Agentes recebem instruções progressivas, arquivos pequenos por slide, skills específicas e checkpoints explícitos. |
| R13 | A raiz pode mudar de caminho sem depender do experimento; cache Python é preparado no uso e não acompanha a distribuição. |
| R14 | Mudança de identidade visual permanece em prévia isolada até aprovação explícita. |
| R15 | O preset geral preserva todos os tipos de exemplo do educacional; docente é adaptado para apresentador. Generalizar não reduz o catálogo. |

## 3. Contrato de entrada e saída

### Projeto de aula
`project.json` usa `schema_version: 1`, título, organização, tema, apresentador,
output `.html`, lista ordenada `slides` e lista opcional `styles`. Caminhos dos
fragmentos/CSS/output são relativos ao próprio manifesto, não ao diretório atual.
O shell e o runtime são fornecidos pela versão instalada deste template.

Cada fragmento deve ter um `section.slide`, `data-layout`, `data-title` e
`aside.speaker-notes`. O conteúdo deve respeitar os componentes/limites em
`docs/CONTRACT.md`. Cada aula pode ter um CSS local, que será embutido.

### Artefato final
Um `.html` independente; pode ser enviado ou copiado para outra pasta sem
tools/src/assets. Hiperlinks bibliográficos são conteúdo, não dependências.
Scripts de teste e checkpoints não são incorporados.

### API pública no navegador
`FormaPresentation` é o nome agnóstico; `AulaTemplate` é um alias compatível.
- `AulaTemplate.goTo(n)`: navegação base 1 com limites.
- `AulaTemplate.current` e `slideCount`: estado somente leitura.
- `AulaTemplate.present()`: alterna apresentação.
- `await AulaTemplate.validate()`: lista de diagnósticos.
- `await AulaTemplate.exportPptx({download:false})`: `Uint8Array` do PPTX.
- `await AulaTemplate.exportPptx()`: gera e dispara o download.

## 4. Limites da conversão

Texto é editável por linha, com runs de formatação. Tabelas e gráficos são
composições de formas/textos, não objetos nativos com dados vinculados. Linhas
exportadas têm geometria editável, sem prometer ancoragem dinâmica aos nós.
Fontes precisam estar disponíveis no destino; motores de texto podem divergir.
O contrato não é um conversor universal de qualquer HTML/CSS/SVG.

Um novo recurso visual deve declarar: representação HTML, mapeamento OOXML,
diagnóstico sem suporte, exemplo mínimo, teste e inspeção visual. A extensão
não pode enfraquecer R01–R06.

## 5. Arquitetura e fonte de verdade

- `src/shell.html`: estrutura, guia de agentes e slots do build.
- `src/general/slides/*.html`: preset geral padrão, não conteúdo específico de cliente.
- `src/slides/*.html`: preset educacional opcional.
- `projects/<aula>/`: brief, storyboard, spec, sessão e fragmentos locais.
- `tools/styles/*.css`: tema e impressão.
- `tools/styles/signal-light.css`: identidade aprovada, independente de previews/.
- `src/components/signal-board.html`: arte expandida pelo build para formas reais no HTML final.
- `tools/runtime/*.js`: módulos IIFE, concatenados num script interno.
- `tools/bundle.json`: ordem explícita dos arquivos incorporados.
- `tools/build.py`: lê fontes, resolve metadados, verifica contrato e compila.
- `tools/browser/audit.js`: harness de teste, nunca bundle de produção.

O hash `forma-build` identifica os inputs; `build.py --check` detecta divergência.
Não edite o HTML gerado e depois execute build esperando preservar o patch.

## 6. Critérios de aceite e evidências

| Requisitos | Evidência |
|---|---|
| R01, R11 | build + self_contained.py + cópia isolada no run_audit |
| R02, R09 | print_pdf.py + pdfinfo em todas as páginas |
| R03, R04, R06 | export_pptx.py + validate_pptx.py + abertura/renderização no LibreOffice |
| R05 | auditoria DOM e caso negativo de elemento canvas |
| R07, R08, R10 | testes de controle com contagem dinâmica; clique real em fullscreen na revisão manual |
| R11 | testes unitários, build determinístico e --check |
| R12 | AGENTS, seis skills e context_pack sem runtime completo |
| R13 | teste de cópia para raiz independente, preparação local e limpeza de bytecode |
| R14 | manifesto/CSS de previews separados; aprovação explícita registrada antes da promoção |
| R15 | cobertura dos tipos no check_structure.py e teste de regressão dos dois catálogos |

Uma entrega aprovada deve ter:
- build sincronizado e contrato estático aprovado;
- auditoria sem overflow nos layouts usados;
- controles e exportação exercitados no navegador;
- ZIP, XML, rels, dimensões, notas e textos editáveis válidos;
- PDF completo com contagem correta e todas as páginas 16:9;
- inspeção visual dos slides afetados;
- limitações e checks não executados declarados.

`validate.py --strict` exige os testes de navegador, Office e pdfinfo. Sem
`--strict`, skips são explícitos. Nem o modo strict substitui uma inspeção visual
ou prova abertura no Microsoft PowerPoint. O headless testa apresentação em
janela, não um gesto de fullscreen real. O relatório deve preservar essa distinção.

## 7. Política de mudança

### Conteúdo
Alterar fragmentos do projeto e CSS local. Atualizar brief/storyboard se mudar
o objetivo. Recompilar e verificar os slides editados.

### Componente compartilhado
Identificar todos os layouts que usam o seletor. Criar caso pequeno, corrigir,
rodar regressão e inspecionar os usos afetados.

### Exportador / impressão / navegação
Registrar spec antes de tocar o runtime, preservar API, executar suíte completa
e comparar saída HTML/PPTX/PDF nos layouts afetados.

### Checkpoint para contexto curto
Salvar objetivo, fase, próximo slide, arquivos alterados, comandos executados,
relatórios, bloqueios e próxima ação em `SESSION.json`. Cada check deve ter
comando e resultado reais, não apenas uma caixa marcada por intenção.

## 8. Fora do escopo atual

Conversão arbitrária de páginas web, fontes web embutidas, animações/transições
PowerPoint, imagens como fallback, planilhas vinculadas e teste automático no
Microsoft PowerPoint. Conteúdo não verificado e bibliografia inventada não são
aceitáveis como dados de uma aula gerada.
