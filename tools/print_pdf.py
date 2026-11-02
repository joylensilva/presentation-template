#!/usr/bin/env python3
"""Imprime o HTML em PDF e confere todas as páginas em 16:9, quando pdfinfo existe."""
import sys
if sys.pycache_prefix is None:
    sys.dont_write_bytecode = True
import argparse
from pathlib import Path
import re
import shutil
import subprocess

from common import DEFAULT_HTML, fail_cli, run_browser, write_json
from self_contained import check
from validate_pptx import require


def inspect_pdf(path, expected_count=None, strict=False):
    if not shutil.which('pdfinfo'):
        if strict:
            raise RuntimeError('pdfinfo obrigatório para conferir páginas e proporção.')
        return {'verified': False, 'reason': 'pdfinfo indisponível'}
    text = subprocess.check_output(['pdfinfo', str(path)], text=True)
    count = int(re.search(r'Pages:\s+(\d+)', text).group(1))
    if expected_count is not None:
        require(count == expected_count, f'PDF tem {count} páginas; esperado {expected_count}.')
    # -f/-l aplica a inspeção a TODAS as páginas, não somente à primeira.
    details = subprocess.check_output(['pdfinfo', '-f', '1', '-l', str(count), str(path)], text=True)
    sizes = re.findall(r'Page\s+\d+ size:\s+([\d.]+) x ([\d.]+) pts', details)
    require(len(sizes) == count, 'pdfinfo não retornou o tamanho de todas as páginas.')
    for width, height in sizes:
        require(abs(float(width)-960) < .1 and abs(float(height)-540) < .1,
                f'Página fora da prancheta 16:9: {width} × {height} pt.')
    return {'verified': True, 'pages': count, 'width_pt': 960, 'height_pt': 540}


def print_pdf(source, output, executable=None, strict=False):
    report = check(source)
    require(report['ok'], '\n'.join(report['errors']))
    output = Path(output).resolve()
    require(output != Path(source).resolve(), 'PDF não pode substituir o HTML.')
    output.parent.mkdir(parents=True, exist_ok=True)
    # Caminho novo impede um arquivo antigo de mascarar falhas do navegador.
    import tempfile
    with tempfile.TemporaryDirectory(prefix='forma-print-') as temp:
        candidate = Path(temp) / 'slides.pdf'
        run_browser(['--no-pdf-header-footer', '--virtual-time-budget=3000',
                     f'--print-to-pdf={candidate}', Path(source).resolve().as_uri()], executable)
        require(candidate.exists(), 'Navegador não produziu PDF.')
        result = inspect_pdf(candidate, report['slides'], strict)
        output.write_bytes(candidate.read_bytes())
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('html', nargs='?', type=Path, default=DEFAULT_HTML)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--browser')
    p.add_argument('--strict', action='store_true')
    p.add_argument('--report', type=Path)
    args = p.parse_args()
    try:
        result = print_pdf(args.html, args.output, args.browser, args.strict)
        if args.report:
            write_json(args.report, result)
        print(f'OK: PDF → {args.output}; verificação: {result}')
    except (ValueError, OSError, RuntimeError, subprocess.SubprocessError) as error:
        fail_cli(error)


if __name__ == '__main__':
    main()
