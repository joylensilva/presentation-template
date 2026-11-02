# Projetos de apresentações

Execute da pasta `presentation-template/`:

```bash
python3 tools/prepare.py
python3 tools/run.py new --directory projects/proposta-01 --title "Minha apresentação"
```

Preencha o brief, storyboard e slides. Depois:

```bash
python3 tools/run.py build --project projects/proposta-01/project.json
python3 tools/run.py validate projects/proposta-01/apresentacao.html --out artifacts/proposta-01 --strict
```

`projects/proposta-01/apresentacao.html` é o único arquivo necessário para distribuir a apresentação.
As fontes de trabalho ficam no projeto; os códigos compartilhados são embutidos pelo build.

O padrão é general. Para apresentações educacionais, acrescente `--preset education`.
Esta pasta integra a raiz independente; o experimento anterior não é dependência.
