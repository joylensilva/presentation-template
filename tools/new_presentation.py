#!/usr/bin/env python3
"""Cria um projeto pequeno a partir de layouts do catálogo; não altera o catálogo."""
import sys
if sys.pycache_prefix is None:
    sys.dont_write_bytecode = True
import argparse
from pathlib import Path

from common import ROOT, fail_cli, preset_paths, read_json, write_json


def create(directory, title, layouts=None, brand='SUA ORGANIZAÇÃO', course='Tema da apresentação', author='Nome do apresentador', preset='general'):
    directory = Path(directory).resolve()
    if directory.exists() and any(directory.iterdir()):
        raise ValueError('Diretório de projeto já contém arquivos; escolha outro nome.')
    source_root, source_project, catalog_path = preset_paths(preset)
    catalog = {entry['layout']: entry for entry in read_json(catalog_path)}
    if layouts is None:
        layouts = [entry['layout'] for entry in catalog.values()]
    unknown = set(layouts) - set(catalog)
    if unknown:
        raise ValueError('Layouts desconhecidos: ' + ', '.join(sorted(unknown)))
    if not layouts:
        raise ValueError('Selecione pelo menos um layout.')
    (directory / 'slides').mkdir(parents=True, exist_ok=True)
    files = []
    for i, layout in enumerate(layouts, 1):
        name = f'slides/{i:02}-{layout}.html'
        files.append(name)
        (directory / name).write_text((source_root / catalog[layout]['file']).read_text(encoding='utf-8'), encoding='utf-8')
    write_json(directory / 'project.json', {'schema_version': 1, 'title': title, 'brand': brand,
        'course': course, 'author': author, 'output': 'apresentacao.html', 'slides': files,
        'styles': ['theme-overrides.css']})
    (directory / 'theme-overrides.css').write_text('/* Personalização desta apresentação. CSS será EMBUTIDO no HTML final. */\n', encoding='utf-8')
    for target, template in [('BRIEF.md','BRIEF.template.md'), ('STORYBOARD.md','STORYBOARD.template.md'),
                             ('CHANGE.spec.md','CHANGE.spec.template.md')]:
        (directory / target).write_text((ROOT / 'tasks' / template).read_text(encoding='utf-8'), encoding='utf-8')
    write_json(directory / 'SESSION.json', {'goal': title, 'phase': 'brief', 'project': 'project.json',
        'next_slide': 1, 'changed_files': [], 'checks': [], 'blockers': [],
        'next_action': 'Preencher BRIEF.md e STORYBOARD.md antes de editar os slides.'})
    (directory / 'AGENTS.md').write_text(
        '# Projeto de apresentação\n\nEste projeto usa a raiz Forma que contém tools/, src/ e AGENTS.md. '
        'Não depende da pasta experimental que a originou. Leia o AGENTS.md dessa raiz '
        'e tools/skills/author-slides/SKILL.md.\n\n'
        'Na primeira rodada: python3 tools/prepare.py. Use python3 tools/run.py para '
        'os comandos, com caminhos relativos à raiz da solução.\n\n'
        'Fonte local: project.json + slides/*.html + theme-overrides.css. '
        'Preencha BRIEF.md e STORYBOARD.md. Retome por SESSION.json.\n\n'
        'O único entregável obrigatório é apresentacao.html, AUTOCONTIDO. '
        'Use tools/build.py --project <caminho deste project.json>. '
        'Não referencie os arquivos de tools em scripts externos no HTML final.\n', encoding='utf-8')
    return directory / 'project.json'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--directory', type=Path, required=True)
    p.add_argument('--title', required=True)
    p.add_argument('--preset', choices=['general', 'education'], default='general')
    p.add_argument('--layouts', nargs='+')
    p.add_argument('--brand', default='SUA ORGANIZAÇÃO')
    p.add_argument('--course', default='Tema da apresentação', help='Tema/linha de rodapé; nome mantido por compatibilidade.')
    p.add_argument('--author', default='Nome do apresentador')
    args = p.parse_args()
    try:
        project = create(args.directory, args.title, args.layouts, args.brand, args.course, args.author, args.preset)
        print(f'OK: projeto criado em {project}. Preencha o brief e os slides; depois execute tools/build.py --project "{project}"')
    except (ValueError, OSError) as error:
        fail_cli(error)


if __name__ == '__main__':
    main()
