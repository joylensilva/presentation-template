"""Testes de regressão do build, do contrato e dos projetos com poucos slides."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
from build import assemble
from common import DEFAULT_PROJECT, ROOT, read_json
from new_presentation import create
from self_contained import check_text


class ToolingTests(unittest.TestCase):
    def test_catalog_build_is_self_contained_and_deterministic(self):
        first, _, info = assemble()
        second, _, _ = assemble()
        self.assertEqual(first, second)
        self.assertTrue(check_text(first)['ok'])
        self.assertEqual(info['slides'], len(read_json(DEFAULT_PROJECT)['slides']))

    def test_external_assets_are_rejected(self):
        source, _, _ = assemble()
        cases = ['<script src="tools/runtime/viewer.js"></script>',
                 '<link rel="stylesheet" href="theme.css">',
                 '<img src="data:image/png;base64,AA==">',
                 '<div style="background:url(assets/x.png)"></div>',
                 '<style>@import "https://example.org/a.css";</style>',
                 '<script>fetch("assets.json")</script>']
        for extra in cases:
            with self.subTest(extra=extra):
                self.assertFalse(check_text(source.replace('</head>', extra + '</head>'))['ok'])

    def test_one_slide_project_and_source_protection(self):
        with tempfile.TemporaryDirectory() as temp:
            project = create(Path(temp) / 'one', 'Aula de teste', ['capa'])
            source, output, info = assemble(project)
            self.assertEqual(info['slides'], 1)
            self.assertIn('<title>Aula de teste</title>', source)
            self.assertTrue(check_text(source)['ok'])
            slide = project.parent / read_json(project)['slides'][0]
            with self.assertRaises(ValueError):
                assemble(project, slide)
            with self.assertRaises(ValueError):
                create(project.parent, 'Não sobrescrever', ['capa'])

    def test_project_specific_css_is_inlined(self):
        with tempfile.TemporaryDirectory() as temp:
            project = create(Path(temp) / 'aula', 'Tema próprio', ['capa', 'sintese'])
            css = ':root{--accent:#123456;}'
            (project.parent / 'theme-overrides.css').write_text(css, encoding='utf-8')
            source, _, _ = assemble(project)
            self.assertIn(css, source)
            self.assertNotIn('<link rel="stylesheet"', source)

    def test_general_is_default_and_education_is_optional(self):
        with tempfile.TemporaryDirectory() as temp:
            general = create(Path(temp) / 'general', 'Revisão executiva')
            teaching = create(Path(temp) / 'education', 'Aula', preset='education')
            self.assertEqual(len(read_json(general)['slides']), len(read_json(ROOT / 'src/general/catalog.json')))
            self.assertEqual(len(read_json(teaching)['slides']), len(read_json(ROOT / 'src/catalog.json')))
            self.assertEqual(read_json(general)['author'], 'Nome do apresentador')
            self.assertIn('Fontes e premissas', (general.parent / read_json(general)['slides'][-2]).read_text())

    def test_general_preserves_every_educational_example_type(self):
        general = read_json(ROOT / 'src/general/catalog.json')
        teaching = read_json(ROOT / 'src/catalog.json')
        general_types = {entry['layout'] for entry in general}
        expected = {'apresentador' if entry['layout'] == 'docente' else entry['layout'] for entry in teaching}
        self.assertEqual(len(general_types), len(general), 'Layouts duplicados no catálogo geral.')
        self.assertTrue(expected.issubset(general_types), f'Exemplos perdidos ao generalizar: {expected - general_types}')
        for entry in general:
            fragment = (ROOT / 'src/general' / entry['file']).read_text(encoding='utf-8')
            self.assertIn(f'data-layout="{entry["layout"]}"', fragment)

    def test_missing_source_does_not_generate_partial_html(self):
        with tempfile.TemporaryDirectory() as temp:
            project = create(Path(temp) / 'aula', 'Teste', ['capa'])
            config = read_json(project)
            config['slides'] = ['slides/inexistente.html']
            project.write_text(json.dumps(config), encoding='utf-8')
            with self.assertRaises(FileNotFoundError):
                assemble(project)
            self.assertFalse((project.parent / 'apresentacao.html').exists())


if __name__ == '__main__':
    unittest.main()
