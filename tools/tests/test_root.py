"""A raiz copiada deve funcionar sem a pasta experimental e sem bytecode distribuído."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import ROOT


class IndependentRootTests(unittest.TestCase):
    def test_root_can_move_and_prepares_its_own_cache(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / 'independent-root'
            shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns(
                '.cache', '__pycache__', '*.pyc', 'artifacts', 'projects',
                'template-aulas.html', 'template-apresentacoes.html'))
            result = subprocess.run([sys.executable, '-B', str(target / 'tools/run.py'), 'build'],
                cwd=temp, capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            html = (target / 'template-apresentacoes.html').read_text(encoding='utf-8')
            self.assertIn('Sistemas conectados.', html)
            self.assertNotIn('<script src=', html)
            self.assertTrue((target / '.cache/ready.json').exists())
            self.assertTrue(list((target / '.cache/python').rglob('*.opt-1.pyc')))
            self.assertFalse(list((target / 'tools').rglob('__pycache__')))
            clean = subprocess.run([sys.executable, '-B', str(target / 'tools/prepare.py'), '--clean'],
                cwd=temp, capture_output=True, text=True, timeout=30)
            self.assertEqual(clean.returncode, 0, clean.stderr)
            self.assertFalse(list(target.rglob('*.pyc')))
            self.assertFalse((target / '.cache/ready.json').exists())


if __name__ == '__main__':
    unittest.main()
