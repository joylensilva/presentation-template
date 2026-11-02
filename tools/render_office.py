#!/usr/bin/env python3
"""Abre PPTX no LibreOffice, renderiza PDF e confirma o resultado em 16:9."""
import sys
if sys.pycache_prefix is None:
    sys.dont_write_bytecode = True
import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile

from common import fail_cli, write_json
from print_pdf import inspect_pdf
from validate_pptx import require, validate


def render(source, output, strict=False):
    office = shutil.which('libreoffice') or shutil.which('soffice')
    if not office:
        raise RuntimeError('LibreOffice não instalado. Não é possível afirmar que o PPTX abriu.')
    package = validate(source)
    output = Path(output).resolve()
    require(output != Path(source).resolve(), 'PDF não pode substituir o PPTX.')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='forma-office-') as temp:
        temp = Path(temp)
        candidate = temp / (Path(source).stem + '.pdf')
        result = subprocess.run([office, f'-env:UserInstallation={(temp / "profile").as_uri()}',
                                 '--headless', '--convert-to', 'pdf', '--outdir', str(temp),
                                 str(Path(source).resolve())], capture_output=True, text=True, timeout=120)
        require(result.returncode == 0 and candidate.exists(), 'LibreOffice não gerou PDF: ' + result.stdout + result.stderr)
        info = inspect_pdf(candidate, package['slides'], strict)
        output.write_bytes(candidate.read_bytes())
    return {'opened_in_libreoffice': True, 'pdf': info}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('pptx', type=Path)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--strict', action='store_true')
    p.add_argument('--report', type=Path)
    args = p.parse_args()
    try:
        result = render(args.pptx, args.output, args.strict)
        if args.report:
            write_json(args.report, result)
        print(f'OK: PPTX aberto no LibreOffice → {args.output}')
    except (ValueError, OSError, RuntimeError, subprocess.SubprocessError) as error:
        fail_cli(error)


if __name__ == '__main__':
    main()
