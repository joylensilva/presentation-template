#!/usr/bin/env python3
"""Confere fontes, catálogo, bundle, skills e links locais da documentação."""
import sys
if sys.pycache_prefix is None:
    sys.dont_write_bytecode = True
import argparse
from pathlib import Path
import re
from urllib.parse import unquote

from build import assemble
from common import ROOT, TOOLS, fail_cli, preset_paths, read_json


def check():
    errors = []
    types = {}
    for preset in ['general', 'education']:
        _, project_path, catalog_path = preset_paths(preset)
        catalog = read_json(catalog_path)
        project = read_json(project_path)
        types[preset] = {entry['layout'] for entry in catalog}
        if len(types[preset]) != len(catalog):
            errors.append(f'{preset}: tipos de layout duplicados.')
        if [e['file'] for e in catalog] != project['slides']:
            errors.append(f'{preset}: catalog.json e project.json divergem em ordem/arquivos.')
    expected = {'apresentador' if key == 'docente' else key for key in types['education']}
    if missing := expected - types['general']:
        errors.append('Exemplos ausentes no preset geral: ' + ', '.join(sorted(missing)))
    bundle = read_json(TOOLS / 'bundle.json')
    for name in bundle['scripts'] + bundle['styles']:
        if not (TOOLS / name).is_file():
            errors.append('Fonte do bundle ausente: ' + name)
        if 'browser/' in name or 'audit' in name:
            errors.append('Harness de teste não pode entrar no bundle: ' + name)
    skills = sorted((TOOLS / 'skills').glob('*/SKILL.md'))
    for skill in skills:
        text = skill.read_text(encoding='utf-8')
        header = re.match(r'^---\n(.*?)\n---\n', text, re.S)
        if not header:
            errors.append('Frontmatter ausente: ' + str(skill))
            continue
        name = re.search(r'^name:\s*(.+)$', header.group(1), re.M)
        description = re.search(r'^description:\s*(.+)$', header.group(1), re.M)
        if not name or name.group(1) != skill.parent.name or not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*', name.group(1)):
            errors.append('Nome inválido de skill: ' + str(skill))
        if not description:
            errors.append('Descrição ausente: ' + str(skill))
    if len(skills) != 6:
        errors.append('O conjunto esperado deve ter seis skills canônicas.')
    for markdown in ROOT.rglob('*.md'):
        if any(part in {'artifacts', 'projects'} for part in markdown.relative_to(ROOT).parts):
            continue
        for link in re.findall(r'\]\(([^)]+)\)', markdown.read_text(encoding='utf-8')):
            if re.match(r'^[a-z]+:|^#', link):
                continue
            target = (markdown.parent / unquote(link.split('#')[0])).resolve()
            if not target.exists():
                errors.append(f'Link quebrado: {markdown.relative_to(ROOT)} → {link}')
    config = read_json(ROOT / 'opencode.json')
    if config.get('skills', {}).get('paths') != ['./tools/skills']:
        errors.append('opencode.json deve registrar tools/skills.')
    assemble()
    return errors, len(skills)


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    try:
        errors, count = check()
        if errors:
            fail_cli('\n'.join(errors))
        print(f'OK: bundle, catálogo, links e {count} skills consistentes.')
    except (ValueError, OSError) as error:
        fail_cli(error)


if __name__ == '__main__':
    main()
