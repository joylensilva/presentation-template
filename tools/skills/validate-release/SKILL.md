---
name: validate-release
description: Use para validar uma apresentação geral ou educacional, exportar os originais e preparar uma entrega Forma verificável.
---
# Validar e entregar

Trabalhe na raiz independente presentation-template/. Comece por `python3 tools/prepare.py`
e prefira `tools/run.py`. General é o preset padrão; education é opcional.
Na distribuição da raiz, rode `tools/prepare.py --clean`: nenhum pyc/cache deve ir junto.
Não promova uma prévia visual sem aprovação explícita.

1. Confirme qual `project.json` e qual HTML são a entrega. Se há build, rode
   `tools/build.py --project <manifesto>` e depois o mesmo comando com `--check`.
2. Execute `python3 tools/doctor.py`. Ferramenta ausente deve ser registrada,
   não substituída por uma alegação de sucesso.
3. Valide:
   ```bash
   python3 tools/self_contained.py projects/aula-01/apresentacao.html
   python3 tools/validate.py projects/aula-01/apresentacao.html --out artifacts/aula-01 --strict
   ```
4. Leia `artifacts/aula-01/report.json`. Confirme contagem variável de slides,
   ausência de media/imagens, notas, textos editáveis e PDF 16:9.
5. Se o usuário pediu PPTX/PDF originais:
   ```bash
   python3 tools/export_pptx.py projects/aula-01/apresentacao.html --output artifacts/aula-original.pptx
   python3 tools/print_pdf.py projects/aula-01/apresentacao.html --output artifacts/aula-original.pdf --strict
   ```
6. Inspecione visualmente os slides alterados. Para coleção completa use
   `tools/contact_sheet.py <PDF> --out artifacts/visual`.
7. Preencha `tasks/REVIEW.template.md` como relatório da entrega e `SESSION.json`.

## Não confundir
`integration-test-only.pptx` tem a capa alterada pelo teste; NUNCA é o entregável.
O HTML deve abrir copiado sozinho. Autocontenção estática + teste isolado dão
evidências disso. Links bibliográficos são permitidos, dependências externas não.
Não diga “validado no Microsoft PowerPoint” sem abri-lo nesse programa.
