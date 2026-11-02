#!/usr/bin/env python3
"""Importação única do HTML Forma anterior; separa fontes sem alterar o original.

Não faz parte do build diário. Recusa substituir qualquer fonte já existente.
"""
import argparse
import json
from pathlib import Path
import re
import textwrap


def extract(source):
    css = re.search(r'<style>\s*(.*?)\s*</style>', source, re.S).group(1)
    js = re.search(r'<script>\s*(.*?)\s*</script>', source, re.S).group(1)
    deck = re.search(r'<main id="deck"[^>]*>(.*?)</main>', source, re.S).group(1)
    sections = re.findall(r'(<!-- GUIA.*?<section class="slide.*?</section>)', deck, re.S)
    if len(sections) != 21:
        raise ValueError('Importador reconhece somente a versão anterior com 21 layouts.')
    result = {}
    entries = []
    for i, section in enumerate(sections, 1):
        layout = re.search(r'data-layout="([^"]+)"', section).group(1)
        title = re.search(r'data-title="([^"]+)"', section).group(1)
        path = f'slides/{i:02}-{layout}.html'
        result[f'src/{path}'] = section.strip() + '\n'
        entries.append({'layout': layout, 'title': title, 'file': path})
    shell = re.sub(r'<style>.*?</style>', '<!-- FORMA:STYLES -->', source, count=1, flags=re.S)
    shell = re.sub(r'<script>.*?</script>', '<!-- FORMA:RUNTIME -->', shell, count=1, flags=re.S)
    shell = shell.replace(deck, '\n<!-- FORMA:SLIDES -->\n')
    shell = re.sub(r'<title>.*?</title>', '<title>{{TITLE}}</title>', shell)
    shell = re.sub(r'<main id="deck"[^>]*>', '<main id="deck" data-brand="{{BRAND}}" data-course="{{COURSE}}" data-author="{{AUTHOR}}">', shell)
    result['src/shell.html'] = shell
    print_at = css.index('@page')
    result['tools/styles/theme.css'] = css[:print_at].rstrip() + '\n'
    result['tools/styles/print.css'] = css[print_at:].strip() + '\n'
    viewer = js[js.index('/* Interface'):js.index('\n/*\n * Exportador')]
    pstart, pend = viewer.index('function showControls'), viewer.index("document.addEventListener('keydown'")
    result['tools/runtime/presentation.js'] = '/* Tela cheia e controles de projeção. */\n' + viewer[pstart:pend]
    result['tools/runtime/print.js'] = '/* Impressão usa o CSS 16:9 embutido pelo build. */\nfunction printSlides(){window.print();}\n$(\'print-button\').onclick=printSlides;\n'
    viewer = viewer[:pstart] + viewer[pend:]
    viewer = viewer.replace("$('print-button').onclick=()=>window.print();\n", '')
    result['tools/runtime/viewer.js'] = viewer.strip() + '\n'

    def chunk(start, end):
        return textwrap.dedent(js[js.index(start):js.index(end)]).strip() + '\n'

    drawing = chunk('  const NS_A=', '  const presets=')
    drawing = drawing.replace('const ENC=new TextEncoder(), UNIT=9525;', 'const UNIT=9525;')
    result['tools/runtime/pptx-drawing.js'] = ('/* DrawingML: geometria, estilos, rich text e links. */\nconst FormaDrawing=(()=>{\n' + drawing +
        '\nreturn {NS_A,NS_P,NS_R,xml,doc,color,solid,stroke,group,rels,geometry,shape,connector,text};\n})();\n')
    dom = chunk('  const presets=', '  const crcTable=') + chunk('  async function measure(', '  async function build(')
    result['tools/runtime/pptx-dom.js'] = ('/* Validação e medição do DOM em 1280 × 720. */\nconst FormaDOM=(()=>{\n'
        'const {color,solid,stroke,geometry,shape,connector,text}=FormaDrawing;\n' + dom + '\nreturn {inspect,render,measure,validate};\n})();\n')
    result['tools/runtime/zip.js'] = ('/* ZIP STORE nativo; sem dependências. */\nconst FormaZip=(()=>{\nconst ENC=new TextEncoder();\n' +
        chunk('  const crcTable=', '  function theme(') + '\nreturn {zip};\n})();\n')
    package = chunk('  function theme(', '  async function measure(') + chunk('  async function build(', '  let exporting=false;')
    package = package.replace('return zip(files);', 'return FormaZip.zip(files);')
    result['tools/runtime/pptx-package.js'] = ('/* Montagem OOXML: apresentação, mestres, slides, tema e notas. */\nconst FormaPackage=(()=>{\n'
        'const {NS_A,NS_P,NS_R,xml,doc,group,rels}=FormaDrawing;\nconst {inspect,render,measure}=FormaDOM;\n' + package + '\nreturn {build};\n})();\n')
    api = chunk('  let exporting=false;', 'window.AulaTemplate=')
    api = api.replace('const bytes=await build();', 'const bytes=await FormaPackage.build();')
    api = api.replace('return {exportPptx,validate};', 'return {exportPptx,validate:FormaDOM.validate};')
    result['tools/runtime/export-pptx.js'] = '/* API de download e feedback da exportação. */\nconst Pptx=(()=>{\n' + api
    result['tools/runtime/bootstrap.js'] = js[js.index('window.AulaTemplate='):].strip() + '\n'
    result['src/catalog.json'] = json.dumps(entries, ensure_ascii=False, indent=2) + '\n'
    result['src/project.json'] = json.dumps({
        'schema_version': 1, 'title': 'Forma — Template de aulas', 'brand': 'SUA INSTITUIÇÃO',
        'course': 'Nome da disciplina', 'author': 'Nome do docente',
        'output': '../template-aulas.html', 'slides': [e['file'] for e in entries],
    }, ensure_ascii=False, indent=2) + '\n'
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--destination', type=Path, required=True)
    args = parser.parse_args()
    files = extract(args.input.read_text(encoding='utf-8'))
    existing = [name for name in files if (args.destination / name).exists()]
    if existing:
        parser.error('Fontes já existem; importação cancelada: ' + ', '.join(existing[:3]))
    for name, text in files.items():
        target = args.destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')
    print(f'Importados {len(files)} arquivos. O HTML original foi preservado.')


if __name__ == '__main__':
    main()
