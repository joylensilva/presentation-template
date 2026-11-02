#!/usr/bin/env python3
"""Inspeção econômica: catálogo, resumo de projeto ou um único fragmento de slide."""
import sys
if sys.pycache_prefix is None:
    sys.dont_write_bytecode = True
import argparse
from pathlib import Path
import re

from common import DEFAULT_PROJECT, ROOT, fail_cli, preset_paths, read_json


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project', type=Path, default=DEFAULT_PROJECT)
    p.add_argument('--catalog', action='store_true')
    p.add_argument('--preset', choices=['general', 'education'], default='general')
    p.add_argument('--layout')
    p.add_argument('--slide', type=int)
    args = p.parse_args()
    try:
        source_root, _, catalog_path = preset_paths(args.preset)
        catalog = read_json(catalog_path)
        if args.layout:
            entry = next((v for v in catalog if v['layout'] == args.layout), None)
            if not entry:
                raise ValueError('Layout inexistente. Use --catalog.')
            print((source_root / entry['file']).read_text(encoding='utf-8'))
        elif args.catalog:
            for i, entry in enumerate(catalog, 1):
                print(f'{i:02} {entry["layout"]:16} {entry["title"]}')
        else:
            project = args.project.resolve()
            data = read_json(project)
            if args.slide is not None:
                if not 1 <= args.slide <= len(data['slides']):
                    raise ValueError('Número de slide fora do projeto.')
                target = project.parent / data['slides'][args.slide-1]
                print(f'<!-- Fonte: {target} -->\n' + target.read_text(encoding='utf-8'))
            else:
                print(f'{data["title"]}: {len(data["slides"])} slides; output={data["output"]}')
                for i, name in enumerate(data['slides'], 1):
                    text = (project.parent / name).read_text(encoding='utf-8')
                    title = re.search(r'data-title="([^"]+)"', text)
                    print(f'{i:02} {name} | {title.group(1) if title else "SEM TÍTULO"}')
    except (ValueError, OSError) as error:
        fail_cli(error)


if __name__ == '__main__':
    main()
