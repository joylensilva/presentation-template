#!/usr/bin/env python3
"""Monta contexto curto para um agente sem carregar o HTML compilado/runtime inteiro."""
import sys
if sys.pycache_prefix is None:
    sys.dont_write_bytecode = True
import argparse
from pathlib import Path

from common import DEFAULT_PROJECT, ROOT, fail_cli, read_json

SKILLS = {'author': 'author-slides', 'layout': 'repair-layout', 'export': 'maintain-pptx',
          'print': 'print-present', 'test': 'validate-release', 'resume': 'resume-work'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--task', choices=SKILLS, default='author')
    p.add_argument('--project', type=Path, default=DEFAULT_PROJECT)
    p.add_argument('--slide', type=int, default=1)
    p.add_argument('--max-chars', type=int, default=16000)
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    try:
        if args.max_chars < 8000:
            raise ValueError('Use pelo menos 8000 caracteres para não omitir o contrato essencial.')
        project = args.project.resolve()
        data = read_json(project)
        if not 1 <= args.slide <= len(data['slides']):
            raise ValueError('Número de slide fora do projeto.')
        session = project.parent / 'SESSION.json'
        if not session.exists():
            session = ROOT / 'SESSION.json'
        paths = [ROOT / 'AGENTS.md', ROOT / f'tools/skills/{SKILLS[args.task]}/SKILL.md',
                 project, session, project.parent / 'BRIEF.md',
                 project.parent / data['slides'][args.slide-1]]
        result = '# Contexto de uma tarefa Forma\n\nFontes modulares são de manutenção; o entregável é UM HTML autocontido.\n'
        omitted = []
        for path in paths:
            if not path.exists():
                continue
            text = path.read_text(encoding='utf-8')
            section = f'\n## {path}\n\n{text}\n'
            if len(result) + len(section) > args.max_chars-1000:
                omitted.append(str(path))
            else:
                result += section
        if omitted:
            result += '\n## Arquivos não incluídos por limite; abra-os sob demanda\n' + '\n'.join('- ' + f for f in omitted)
        result += '\n\nNão presuma conteúdo dos arquivos omitidos. Faça uma etapa, registre SESSION.json e valide.\n'
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(result, encoding='utf-8')
            print(f'OK: {len(result)} caracteres, {len(omitted)} arquivos omitidos → {args.output}')
        else:
            print(result)
    except (ValueError, OSError) as error:
        fail_cli(error)


if __name__ == '__main__':
    main()
