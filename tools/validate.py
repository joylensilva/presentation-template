#!/usr/bin/env python3
"""Pipeline integrado: autocontenção, DOM, controles, PPTX, PDF e Office opcional."""
import sys
if sys.pycache_prefix is None:
    sys.dont_write_bytecode = True
import argparse
import base64
from pathlib import Path
import shutil
import subprocess

from common import DEFAULT_HTML, ROOT, fail_cli, run_audit, write_json
from print_pdf import print_pdf
from render_office import render
from self_contained import check
from validate_pptx import require, validate


def pipeline(source, output, executable=None, strict=False):
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    report = {'ok': False, 'html': str(Path(source).resolve())}
    try:
        report['static'] = check(source)
        require(report['static']['ok'], '\n'.join(report['static']['errors']))
        browser = run_audit(source, 'integration', executable)
        binary = base64.b64decode(browser.pop('pptx'), validate=True)
        report['browser'] = browser
        # O teste modifica a capa: seu PPTX NÃO é o entregável de produção.
        pptx = output / 'integration-test-only.pptx'
        pptx.write_bytes(binary)
        report['pptx'] = validate(pptx, browser['count'], 'FORMA42' if browser.get('mutated') else None)
        report['print'] = print_pdf(source, output / 'html-print.pdf', executable, strict)
        has_office = shutil.which('libreoffice') or shutil.which('soffice')
        if has_office:
            report['office'] = render(pptx, output / 'pptx-render.pdf', strict)
        elif strict:
            raise RuntimeError('LibreOffice obrigatório em --strict.')
        else:
            report['office'] = {'verified': False, 'reason': 'LibreOffice indisponível'}
        report['ok'] = True
        return report
    except Exception as error:
        report['error'] = str(error)
        raise
    finally:
        write_json(output / 'report.json', report)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('html', nargs='?', type=Path, default=DEFAULT_HTML)
    p.add_argument('--out', type=Path, default=ROOT / 'artifacts/validation')
    p.add_argument('--browser')
    p.add_argument('--strict', action='store_true', help='Exige LibreOffice e pdfinfo; não admite skips.')
    args = p.parse_args()
    try:
        report = pipeline(args.html, args.out, args.browser, args.strict)
        print(f'OK: {report["pptx"]["slides"]} slides, {report["pptx"]["text_boxes"]} textos editáveis; relatório: {args.out / "report.json"}')
        if not report['office'].get('opened_in_libreoffice'):
            print('SKIP: abertura Office não verificada; consulte report.json.')
    except (ValueError, OSError, RuntimeError, subprocess.SubprocessError) as error:
        fail_cli(error)


if __name__ == '__main__':
    main()
