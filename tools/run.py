#!/usr/bin/env python3
"""Executa ferramentas usando a raiz independente e o cache preparado localmente."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
COMMANDS = {'build': 'build.py', 'new': 'new_presentation.py', 'inspect': 'inspect_slides.py',
    'context': 'context_pack.py', 'doctor': 'doctor.py', 'structure': 'check_structure.py',
    'standalone': 'self_contained.py', 'validate': 'validate.py', 'export': 'export_pptx.py',
    'pptx-check': 'validate_pptx.py', 'print': 'print_pdf.py', 'office': 'render_office.py',
    'screenshot': 'screenshot.py', 'contact': 'contact_sheet.py'}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in {'-h', '--help'}:
        print('Uso: python3 tools/run.py COMANDO [argumentos]\nComandos: ' + ', '.join([*COMMANDS, 'test']))
        return
    command = sys.argv[1]
    if command not in {*COMMANDS, 'test'}:
        raise SystemExit('Comando desconhecido; consulte --help.')
    subprocess.run([sys.executable, '-B', str(ROOT / 'tools/prepare.py')], cwd=ROOT, check=True)
    prefix = [sys.executable, '-O', '-X', f'pycache_prefix={ROOT / ".cache/python"}']
    target = ['-m', 'unittest', 'discover', '-s', 'tools/tests', '-v'] if command == 'test' else [str(ROOT / 'tools' / COMMANDS[command])]
    raise SystemExit(subprocess.run([*prefix, *target, *sys.argv[2:]], cwd=ROOT).returncode)


if __name__ == '__main__':
    main()
