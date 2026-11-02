#!/usr/bin/env python3
"""Compila fontes modulares em UM HTML autocontido, sem dependências externas."""
import sys
if sys.pycache_prefix is None:
    sys.dont_write_bytecode = True
import argparse
import hashlib
import html
from pathlib import Path

from common import DEFAULT_PROJECT, ROOT, TOOLS, fail_cli, read_json, write_json
from self_contained import check_text


def assemble(project_path=DEFAULT_PROJECT, output_override=None):
    project_path = Path(project_path).resolve()
    project = read_json(project_path)
    if not isinstance(project, dict):
        raise ValueError('Manifesto deve ser um objeto JSON.')
    unknown = set(project) - {'schema_version', 'title', 'brand', 'course', 'author', 'output', 'slides', 'styles'}
    if unknown:
        raise ValueError('Campos desconhecidos no manifesto: ' + ', '.join(sorted(unknown)))
    if project.get('schema_version') != 1:
        raise ValueError('schema_version deve ser 1.')
    for field in ['title', 'brand', 'course', 'author', 'output', 'slides']:
        if not project.get(field):
            raise ValueError('Campo obrigatório vazio: ' + field)
    for field in ['title', 'brand', 'course', 'author', 'output']:
        if not isinstance(project[field], str) or not project[field].strip():
            raise ValueError('Campo deve ser texto não vazio: ' + field)
    if not isinstance(project['slides'], list) or not all(isinstance(v, str) for v in project['slides']):
        raise ValueError('slides deve ser uma lista de caminhos HTML.')
    if not all(v.endswith('.html') for v in project['slides']):
        raise ValueError('Fragmentos de slide devem ter extensão .html.')
    if not isinstance(project.get('styles', []), list) or not all(isinstance(v, str) and v.endswith('.css') for v in project.get('styles', [])):
        raise ValueError('styles deve ser uma lista de caminhos CSS.')
    bundle = read_json(TOOLS / 'bundle.json')
    inputs = [ROOT / 'src/shell.html', ROOT / 'src/components/signal-board.html']
    inputs += [(project_path.parent / name).resolve() for name in project['slides']]
    extra_styles = [(project_path.parent / name).resolve() for name in project.get('styles', [])]
    inputs += [TOOLS / name for name in bundle['styles'] + bundle['scripts']] + extra_styles
    for path in inputs:
        if not path.is_file():
            raise FileNotFoundError(path)
    texts = {path: path.read_text(encoding='utf-8') for path in inputs}
    digest = hashlib.sha256()
    digest.update(project_path.read_bytes())
    digest.update((TOOLS / 'bundle.json').read_bytes())
    for path in inputs:
        digest.update(texts[path].encode('utf-8'))
    source = texts[ROOT / 'src/shell.html']
    for key in ['title', 'brand', 'course', 'author']:
        source = source.replace('{{' + key.upper() + '}}', html.escape(str(project[key]), quote=True))
    fragments = []
    for name in project['slides']:
        fragment = texts[(project_path.parent / name).resolve()]
        if fragment.count('<section ') != 1 or 'class="slide' not in fragment:
            raise ValueError(f'Cada fragmento deve conter exatamente um slide: {name}')
        fragment = fragment.replace('<!-- FORMA:SIGNAL_ART -->', texts[ROOT / 'src/components/signal-board.html'].strip())
        fragments.append(fragment.strip())
    css = '\n'.join(f'/* fonte: tools/{name} */\n{texts[TOOLS / name]}' for name in bundle['styles'])
    css += '\n' + '\n'.join(texts[path] for path in extra_styles)
    js = '\n'.join(f'/* fonte: tools/{name} */\n{texts[TOOLS / name]}' for name in bundle['scripts'])
    if '</script' in js.lower() or '</style' in css.lower():
        raise ValueError('Fonte contém fechamento de script/style e não pode ser embutida literalmente.')
    replacements = {'STYLES': '<style>\n' + css + '\n</style>',
                    'SLIDES': '\n\n'.join(fragments),
                    'RUNTIME': '<script>\n\'use strict\';\n' + js + '\n</script>'}
    for key, value in replacements.items():
        marker = '<!-- FORMA:' + key + ' -->'
        if source.count(marker) != 1:
            raise ValueError(f'Marcador obrigatório duplicado/ausente: {marker}')
        source = source.replace(marker, value)
    source = source.replace('</head>', f'<meta name="forma-build" content="{digest.hexdigest()}">\n</head>')
    result = check_text(source)
    if not result['ok']:
        raise ValueError('\n'.join(result['errors']))
    output = Path(output_override).resolve() if output_override else (project_path.parent / project['output']).resolve()
    if output.suffix.lower() != '.html':
        raise ValueError('O artefato final deve ter extensão .html.')
    if output in [*inputs, project_path, TOOLS / 'bundle.json']:
        raise ValueError('O output não pode substituir uma fonte ou manifesto.')
    return source, output, {'slides': result['slides'], 'sha256_inputs': digest.hexdigest(),
                            'source_files': len(inputs), 'output': str(output)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project', type=Path, default=DEFAULT_PROJECT)
    p.add_argument('--output', type=Path)
    p.add_argument('--check', action='store_true', help='Falha se o HTML estiver desatualizado; não grava.')
    p.add_argument('--report', type=Path)
    args = p.parse_args()
    try:
        source, output, report = assemble(args.project, args.output)
        if args.check:
            if not output.exists() or output.read_text(encoding='utf-8') != source:
                raise ValueError('HTML desatualizado. Execute tools/build.py para recompilar.')
        else:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(source, encoding='utf-8')
        report['output'] = str(output)
        if args.report:
            write_json(args.report, report)
        print(f'OK: {report["slides"]} slides; HTML {"sincronizado" if args.check else "gerado"}: {output}')
    except (ValueError, OSError) as error:
        fail_cli(error)


if __name__ == '__main__':
    main()
