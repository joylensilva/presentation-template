# Testes e validações

Padrão atual: preset geral com 21 layouts; educação é opcional, também com 21. Execute
`python3 tools/prepare.py` na primeira rodada e use `python3 tools/run.py test`.
O teste de portabilidade copia a raiz sem o experimento, gera o HTML, prepara
cache próprio e verifica sua limpeza. Não distribua `__pycache__`, `.pyc` ou `.cache/`.
O teste de cobertura dos tipos impede que a generalização remova exemplos do
educacional: `docente` é adaptado a `apresentador`, e os outros tipos são preservados.
Os registros anteriores de 21 layouts permanecem históricos em VALIDATION.md.

## Camadas independentes

1. **Build:** fontes presentes, um fragmento por slide, slots resolvidos, conteúdo
   embutido e resultado determinístico. `--check` verifica sincronização.
2. **Contrato estático:** sem assets/script/CSS externos; controles, notas e API.
3. **Navegador:** runtime real numa cópia isolada; DOM, overflow e controles.
4. **PPTX estrutural:** ZIP/CRC, XML bem-formado, content types, relationships,
   IDs únicos, notas, texto, conectores, tamanho e ausência de media/imagens.
5. **Impressão:** PDF do HTML, contagem e 960×540 pt em TODAS as páginas.
6. **Office:** abertura e renderização do PPTX no LibreOffice; PDF novamente medido.
7. **Visual/manual:** composição, legibilidade e fullscreen com clique confiável.

Nenhuma dessas camadas isoladamente comprova todas as outras.

## Executar

```bash
python3 tools/build.py
python3 tools/build.py --check
python3 -m unittest discover -s tools/tests -v
python3 tools/validate.py --strict
```

Para aulas, forneça o HTML gerado a `validate.py`; não há exigência de 21 slides.
`--out` seleciona a pasta de evidências. `--strict` falha se Office/pdfinfo estiverem
ausentes; sem ele, o relatório informa skips sem fingir verificação.

## Distinção crítica: integração e produção

O harness de integração muda um título para `FORMA42` e verifica esse texto no
PPTX. Isso prova que o arquivo reflete o DOM atual. Por isso o arquivo se chama
**`integration-test-only.pptx`** e não deve ser distribuído como aula.

Para o original:
```bash
python3 tools/export_pptx.py --output artifacts/original.pptx --report artifacts/original-export.json
python3 tools/render_office.py artifacts/original.pptx --output artifacts/original-office.pdf --strict
```

O modo `export` do harness não altera o conteúdo. O PDF HTML do pipeline também
é do documento original, mas o PDF Office do pipeline é da versão de integração.
Compare os originais quando precisar de paridade visual incluindo a capa.

## O que o teste de controles cobre

Navegação por API e setas, Home/End, seletor, notas, apresentação em janela,
proporção uniforme, saída do modo apresentação, rejeição de canvas e remoção da
área de medição. O teste conserva o slide ativo após exportar.

A Fullscreen API é explicitamente recusada pelo harness para testar a alternativa
em janela. Fullscreen real exige um gesto confiável do usuário: clique no botão,
verifique barra oculta, mova o mouse até o topo e use Esc. Registre como manual.

## Revisão visual

```bash
python3 tools/screenshot.py --slide 11 --output artifacts/slide-11.png
python3 tools/print_pdf.py --output artifacts/original-html.pdf --strict
python3 tools/contact_sheet.py artifacts/original-html.pdf --out artifacts/visual-html
python3 tools/contact_sheet.py artifacts/original-office.pdf --out artifacts/visual-office
```

Inspecione: títulos e quebras, alinhamento de ícones, espaços, listas, diagramas,
bordas, legibilidade e rodapé. Compare também os slides que compartilham um
componente alterado. Diferenças de fonte podem ser de motor de renderização,
mas cortes ou perda de texto exigem correção.

## Testes do tooling

`tools/tests/test_tooling.py` cobre build determinístico, recursos externos
proibidos, CSS local embutido, projeto de um slide, preservação das fontes e
ausência de HTML parcial quando uma fonte não existe. Só biblioteca padrão.

## Relatórios e entrega

`report.json` contém `ok`, HTML-alvo, check estático, testes do navegador,
estatísticas OOXML, verificação de impressão e abertura Office. Falhas também
produzem relatório. Não confie em arquivos antigos de teste: os CLIs de PDF e
Office verificam um candidato temporário novo antes de salvar a saída.

Preencha `tasks/REVIEW.template.md` com comandos, resultados e lacunas. Microsoft
PowerPoint deve constar como NÃO EXECUTADO se não foi aberto nesse aplicativo.
