#!/usr/bin/env python3
"""Executa o exportador JavaScript embutido e salva um PPTX sem alterar o conteúdo."""
import sys
if sys.pycache_prefix is None:
    sys.dont_write_bytecode = True
import argparse
import base64
from pathlib import Path

from common import DEFAULT_HTML, fail_cli, run_audit, write_json
from self_contained import check
from validate_pptx import require, validate


def export(source, output, executable=None):
    static = check(source)
    require(static['ok'], '\n'.join(static['errors']))
    report = run_audit(source, 'export', executable)
    binary = base64.b64decode(report.pop('pptx'), validate=True)
    output = Path(output).resolve()
    require(output != Path(source).resolve(), 'PPTX não pode substituir o HTML.')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(binary)
    return {'browser': report, 'package': validate(output, report['count'])}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('html', nargs='?', type=Path, default=DEFAULT_HTML)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--browser')
    p.add_argument('--report', type=Path)
    args = p.parse_args()
    try:
        result = export(args.html, args.output, args.browser)
        if args.report:
            write_json(args.report, result)
        print(f'OK: PPTX original, {result["package"]["slides"]} slides → {args.output}')
    except (ValueError, OSError, RuntimeError) as error:
        fail_cli(error)


if __name__ == '__main__':
    main()
