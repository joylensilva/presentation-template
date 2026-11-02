#!/usr/bin/env python3
"""Mostra disponibilidade de ferramentas sem instalar ou alterar o ambiente."""
import sys
if sys.pycache_prefix is None:
    sys.dont_write_bytecode = True
import argparse
import platform
import shutil

from common import browser_path, fail_cli


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--strict', action='store_true')
    args = p.parse_args()
    print('Python:', platform.python_version(), '(3.10+ recomendado)')
    missing = []
    try:
        print('Navegador:', browser_path())
    except RuntimeError as error:
        print('Navegador: AUSENTE'); missing.append(str(error))
    for name in ['libreoffice', 'pdfinfo', 'pdftoppm']:
        found = shutil.which(name)
        print(name + ':', found or 'AUSENTE')
        if not found:
            missing.append(name)
    print('Node/npm/pip: não necessários. Runtime final: somente navegador.')
    if args.strict and missing:
        fail_cli('Ferramentas ausentes: ' + ', '.join(missing))


if __name__ == '__main__':
    main()
