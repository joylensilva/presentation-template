#!/usr/bin/env python3
"""Captura um slide no navegador para revisão visual; não é a exportação PPTX."""
import sys
if sys.pycache_prefix is None:
    sys.dont_write_bytecode = True
import argparse
from pathlib import Path
import tempfile

from common import DEFAULT_HTML, fail_cli, run_browser
from self_contained import check
from validate_pptx import require


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('html', nargs='?', type=Path, default=DEFAULT_HTML)
    p.add_argument('--slide', type=int, default=1)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--browser')
    args = p.parse_args()
    try:
        info = check(args.html)
        require(info['ok'], '\n'.join(info['errors']))
        require(1 <= args.slide <= info['slides'], 'Slide fora da apresentação.')
        target = args.output.resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='forma-screenshot-') as temp:
            candidate = Path(temp) / 'slide.png'
            run_browser(['--window-size=1440,900', '--hide-scrollbars', '--virtual-time-budget=1000',
                         f'--screenshot={candidate}', args.html.resolve().as_uri() + f'#{args.slide}'], args.browser)
            require(candidate.exists(), 'Captura não foi gerada.')
            target.write_bytes(candidate.read_bytes())
        print(f'OK: slide {args.slide} → {target}')
    except (ValueError, OSError, RuntimeError) as error:
        fail_cli(error)


if __name__ == '__main__':
    main()
