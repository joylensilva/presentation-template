#!/usr/bin/env python3
"""Primeira rodada: verifica sintaxe e prepara bytecode local otimizado (nível 1)."""
import sys
sys.dont_write_bytecode = True
import argparse
import compileall
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / 'tools'
CACHE = ROOT / '.cache'


def clean():
    count = 0
    for base in [TOOLS, CACHE / 'python']:
        if not base.exists():
            continue
        for path in base.rglob('*.pyc'):
            path.unlink()
            count += 1
        for directory in sorted(base.rglob('*'), key=lambda p: len(p.parts), reverse=True):
            if directory.is_dir() and not any(directory.iterdir()):
                directory.rmdir()
    if (CACHE / 'python').exists() and not any((CACHE / 'python').iterdir()):
        (CACHE / 'python').rmdir()
    (CACHE / 'ready.json').unlink(missing_ok=True)
    if CACHE.exists() and not any(CACHE.iterdir()):
        CACHE.rmdir()
    return count


def prepare():
    digest = hashlib.sha256((sys.version + str(ROOT)).encode())
    sources = sorted(TOOLS.rglob('*.py'))
    for path in sources:
        digest.update(path.relative_to(ROOT).as_posix().encode())
        digest.update(path.read_bytes())
    fingerprint = digest.hexdigest()
    stamp = CACHE / 'ready.json'
    if stamp.exists():
        previous = json.loads(stamp.read_text(encoding='utf-8'))
        if previous.get('fingerprint') == fingerprint and (CACHE / 'python').is_dir():
            print('OK: bytecode local atualizado; reutilizando cache desta instalação.')
            return
    # Sem __pycache__ em tools/: o prefixo guarda tudo na área local descartável.
    sys.pycache_prefix = str(CACHE / 'python')
    sys.dont_write_bytecode = False
    if not compileall.compile_dir(str(TOOLS), quiet=1, optimize=1, force=False):
        raise RuntimeError('Há erro de sintaxe nas ferramentas; preparação interrompida.')
    CACHE.mkdir(exist_ok=True)
    stamp.write_text(json.dumps({'fingerprint': fingerprint, 'optimization': 1,
        'python': sys.version.split()[0], 'source_files': len(sources),
        'root': str(ROOT)}, indent=2) + '\n', encoding='utf-8')
    print(f'OK: {len(sources)} fontes preparadas em .cache/python, otimização 1.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--clean', action='store_true', help='Remove somente bytecode/cache gerado antes de distribuir a raiz.')
    args = parser.parse_args()
    if args.clean:
        print(f'OK: {clean()} arquivos de bytecode removidos. A próxima rodada executará prepare.py.')
    else:
        prepare()


if __name__ == '__main__':
    main()
