#!/usr/bin/env python3
"""Detecta dependências externas e confirma o contrato de entrega autocontida."""
import sys
if sys.pycache_prefix is None:
    sys.dont_write_bytecode = True
import argparse
from html.parser import HTMLParser
from pathlib import Path
import re

from common import DEFAULT_HTML, fail_cli, write_json


class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.errors = []
        self.slide_count = 0
        self.notes_count = 0
        self.scripts = 0
        self.ids = set()
        self.deck = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids:
                self.errors.append('ID duplicado: ' + a['id'])
            self.ids.add(a['id'])
        classes = a.get('class', '').split()
        if re.search(r'\burl\s*\(|@import\b', a.get('style', ''), re.I):
            self.errors.append('Recurso externo/imagem em atributo style.')
        if tag == 'section' and 'slide' in classes:
            self.slide_count += 1
            for key in ['data-layout', 'data-title']:
                if not a.get(key):
                    self.errors.append(f'Slide {self.slide_count} sem {key}.')
        self.notes_count += int('speaker-notes' in classes)
        self.deck |= a.get('id') == 'deck'
        if tag == 'script':
            self.scripts += 1
            if a.get('src') or a.get('type') == 'module':
                self.errors.append('Script externo/module proibido no artefato final.')
        if tag in {'img', 'iframe', 'object', 'embed', 'video', 'audio', 'canvas', 'source'}:
            self.errors.append(f'Elemento incompatível com o contrato vetorial: <{tag}>.')
        if tag == 'link' and a.get('rel', '').lower() not in {'canonical', 'alternate'}:
            self.errors.append('<link> de recurso externo não pode estar no artefato final.')
        for key in ['src', 'srcset', 'poster', 'data']:
            if a.get(key):
                self.errors.append(f'Recurso referenciado em {tag}[{key}].')
        if tag not in {'a', 'link'} and (a.get('href') or a.get('xlink:href')):
            self.errors.append(f'Referência externa em <{tag}>; use formas reais.')


def check_text(source):
    parsed = Document()
    parsed.feed(source)
    errors = list(parsed.errors)
    if not parsed.deck or parsed.slide_count == 0:
        errors.append('Documento precisa de #deck e pelo menos um slide.')
    if parsed.notes_count != parsed.slide_count:
        errors.append('Cada slide deve ter uma seção speaker-notes.')
    required = {'viewport', 'deck', 'prev', 'next', 'counter', 'slide-picker', 'notes-button',
                'notes-drawer', 'notes-content', 'print-button', 'present-button', 'export-button', 'status'}
    missing = required - parsed.ids
    if missing:
        errors.append('Controles ausentes: ' + ', '.join(sorted(missing)))
    if parsed.scripts == 0 or 'window.AulaTemplate=' not in source:
        errors.append('Runtime completo/API AulaTemplate ausente.')
    for marker, label in [
        (r'@import\b', 'CSS @import'), (r'\burl\s*\(', 'CSS url()'),
        (r'\bfetch\s*\(', 'fetch'), (r'\bXMLHttpRequest\b', 'XMLHttpRequest'),
        (r'\bWebSocket\s*\(', 'WebSocket'), (r'\bimport\s*\(', 'import dinâmico'),
        (r'\bimportScripts\s*\(', 'importScripts'), (r'\bnew\s+(?:Worker|SharedWorker)\s*\(', 'Worker'),
        (r'\b(?:navigator\.)?serviceWorker\b', 'ServiceWorker'),
    ]:
        # Comentários/instruções não são código; manter o lint de código conservador.
        code = '\n'.join(re.findall(r'<(?:style|script)\b[^>]*>(.*?)</(?:style|script)>', source, re.S | re.I))
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.S)
        if re.search(marker, code):
            errors.append(f'Dependência/recurso proibido no código final: {label}.')
    if re.search(r'<!-- FORMA:(?:STYLES|SLIDES|RUNTIME|SIGNAL_ART) -->|\{\{(?:TITLE|BRAND|COURSE|AUTHOR)\}\}', source):
        errors.append('Marcador de build não resolvido.')
    if '@page' not in source or 'screen16x9' not in source or 'window.print()' not in source:
        errors.append('Código de impressão/exportação 16:9 incompleto.')
    return {'ok': not errors, 'slides': parsed.slide_count, 'notes': parsed.notes_count,
            'external_dependencies': len(parsed.errors), 'errors': errors}


def check(path):
    return check_text(Path(path).read_text(encoding='utf-8'))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('html', nargs='?', type=Path, default=DEFAULT_HTML)
    p.add_argument('--report', type=Path)
    args = p.parse_args()
    result = check(args.html)
    if args.report:
        write_json(args.report, result)
    if not result['ok']:
        fail_cli('\n'.join(result['errors']))
    print(f'OK: {result["slides"]} slides, {result["notes"]} notas; HTML autocontido.')


if __name__ == '__main__':
    main()
