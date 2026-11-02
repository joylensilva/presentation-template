#!/usr/bin/env python3
"""Confere ZIP, OOXML, relacionamentos, notas, proporção e editabilidade."""
import sys
if sys.pycache_prefix is None:
    sys.dont_write_bytecode = True
import argparse
from pathlib import Path
import posixpath
import xml.etree.ElementTree as ET
import zipfile

from common import fail_cli, write_json

NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(path, expected_count=None, expected_text=None):
    with zipfile.ZipFile(path) as z:
        require(z.testzip() is None, 'ZIP com CRC inválido.')
        names = set(z.namelist())
        require(len(names) == len(z.namelist()), 'Partes duplicadas no ZIP.')
        trees = {n: ET.fromstring(z.read(n)) for n in names if n.endswith(('.xml', '.rels'))}
        ct = trees['[Content_Types].xml']
        overrides = {n.get('PartName').lstrip('/') for n in ct if n.tag.endswith('Override')}
        defaults = {n.get('Extension') for n in ct if n.tag.endswith('Default')}
        for name in names - {'[Content_Types].xml'}:
            require(name in overrides or name.rsplit('.', 1)[-1] in defaults, f'ContentType ausente: {name}')
        for name in overrides:
            require(name in names, f'ContentType aponta para parte inexistente: {name}')
        for name, tree in trees.items():
            if not name.endswith('.rels'):
                continue
            base = posixpath.dirname(posixpath.dirname(name)) if name != '_rels/.rels' else ''
            ids = [rel.get('Id') for rel in tree]
            require(len(ids) == len(set(ids)), f'IDs de relacionamento repetidos em {name}')
            for rel in tree:
                if rel.get('TargetMode') == 'External':
                    continue
                target = rel.get('Target')
                resolved = target.lstrip('/') if target.startswith('/') else posixpath.normpath(posixpath.join(base, target))
                require(resolved in names, f'Relacionamento inválido: {name} → {resolved}')
        presentation = trees['ppt/presentation.xml']
        count = len(presentation.find('p:sldIdLst', NS))
        require(count > 0, 'PPTX vazio.')
        if expected_count is not None:
            require(count == expected_count, f'Esperados {expected_count} slides; recebidos {count}.')
        size = presentation.find('p:sldSz', NS)
        require((int(size.get('cx')), int(size.get('cy'))) == (12192000, 6858000), 'Prancheta PPTX difere de 16:9 / 1280×720.')
        require(not any(n.startswith('ppt/media/') for n in names), 'PPTX contém imagens/media; contrato editável violado.')
        stats = {'slides': count, 'shapes': 0, 'text_boxes': 0, 'connectors': 0, 'notes': 0,
                 'images': 0, 'external_links': 0, 'parts': len(names), 'all_text': ''}
        for i in range(1, count+1):
            path = f'ppt/slides/slide{i}.xml'
            tree = trees[path]
            require(not tree.findall('.//p:pic', NS), f'Imagem no slide {i}.')
            for tag, key in [('sp','shapes'), ('txBody','text_boxes'), ('cxnSp','connectors')]:
                stats[key] += len(tree.findall('.//p:' + tag, NS))
            ids = [n.get('id') for n in tree.findall('.//p:cNvPr', NS)]
            require(len(ids) == len(set(ids)), f'IDs de forma repetidos no slide {i}.')
            notes = f'ppt/notesSlides/notesSlide{i}.xml'
            require(notes in trees, f'Notas ausentes no slide {i}.')
            stats['notes'] += 1
            require(tree.findall('.//a:t', NS), f'Slide {i} não contém texto editável.')
            stats['all_text'] += '\n'.join(n.text or '' for n in tree.findall('.//a:t', NS)) + '\n'
            reltree = trees[f'ppt/slides/_rels/slide{i}.xml.rels']
            relids = {r.get('Id') for r in reltree}
            for node in tree.iter():
                for key in ['{' + NS['r'] + '}id', '{' + NS['r'] + '}embed']:
                    if key in node.attrib:
                        require(node.attrib[key] in relids, f'Relationship não resolvido no slide {i}.')
            stats['external_links'] += sum(r.get('TargetMode') == 'External' for r in reltree)
        if expected_text:
            require(expected_text in stats['all_text'], 'Texto alterado no DOM não foi exportado.')
        del stats['all_text']
        return {'ok': True, **stats}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('pptx', type=Path)
    p.add_argument('--expected-count', type=int)
    p.add_argument('--report', type=Path)
    args = p.parse_args()
    try:
        result = validate(args.pptx, args.expected_count)
        if args.report:
            write_json(args.report, result)
        print(result)
    except (ValueError, OSError, KeyError, ET.ParseError, zipfile.BadZipFile) as error:
        fail_cli(error)


if __name__ == '__main__':
    main()
