#!/usr/bin/env python3
"""Renderiza um PDF em PNGs e gera índice HTML sem dependências Python externas."""
import sys
if sys.pycache_prefix is None:
    sys.dont_write_bytecode = True
import argparse
import html
from pathlib import Path
import shutil
import subprocess
import tempfile

from common import fail_cli


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('pdf', type=Path)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    try:
        tool = shutil.which('pdftoppm')
        if not tool:
            raise RuntimeError('pdftoppm não instalado. Use Poppler para a revisão visual.')
        args.out.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='forma-contact-') as temp:
            prefix = Path(temp) / args.pdf.stem
            subprocess.run([tool, '-scale-to', '640', '-png', str(args.pdf), str(prefix)], check=True, capture_output=True, timeout=120)
            images = []
            for rendered in sorted(Path(temp).glob(args.pdf.stem + '-*.png')):
                target = args.out / rendered.name
                shutil.copyfile(rendered, target)
                images.append(target)
        cards = ''.join(f'<figure><figcaption>{html.escape(p.stem)}</figcaption><img src="{html.escape(p.name, quote=True)}" alt="{html.escape(p.stem, quote=True)}"></figure>' for p in images)
        page = '<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Revisão visual</title><style>body{font:14px Arial;background:#e7ebed;padding:20px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px}figure{margin:0}img{width:100%}figcaption{padding:8px}</style><h1>Revisão visual — ' + html.escape(args.pdf.name) + '</h1><main>' + cards + '</main></html>'
        (args.out / 'index.html').write_text(page, encoding='utf-8')
        print(f'OK: {len(images)} páginas → {args.out / "index.html"}. Índice de teste, não entregável de apresentação.')
    except (OSError, RuntimeError, subprocess.SubprocessError) as error:
        fail_cli(error)


if __name__ == '__main__':
    main()
