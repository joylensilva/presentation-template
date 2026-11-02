"""Infraestrutura compartilhada dos CLIs. Somente biblioteca padrão Python."""
import sys
# Execução direta continua válida; não distribua __pycache__ junto das fontes.
if sys.pycache_prefix is None:
    sys.dont_write_bytecode = True
import html
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / 'tools'
DEFAULT_HTML = ROOT / 'template-apresentacoes.html'
DEFAULT_PROJECT = ROOT / 'src/general/project.json'


def preset_paths(name='general'):
    if name not in {'general', 'education'}:
        raise ValueError('Preset deve ser general ou education.')
    directory = ROOT / 'src/general' if name == 'general' else ROOT / 'src'
    return directory, directory / 'project.json', directory / 'catalog.json'


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def browser_path(explicit=None):
    if explicit or os.environ.get('FORMA_BROWSER'):
        candidate = explicit or os.environ['FORMA_BROWSER']
        executable = shutil.which(str(candidate))
        if executable:
            return executable
        raise RuntimeError(f'Navegador não encontrado: {candidate}')
    for name in ['brave-browser', 'chromium', 'chromium-browser', 'google-chrome']:
        if executable := shutil.which(name):
            return executable
    raise RuntimeError('Instale Brave/Chromium ou defina FORMA_BROWSER com o executável.')


def run_browser(args, executable=None, timeout=120):
    # Headless cria seu próprio perfil temporário. --user-data-dir causou travamento
    # no Brave 156 deste ambiente; não reutilizar o perfil do navegador do usuário.
    cmd = [browser_path(executable), '--headless=new', '--no-sandbox', '--disable-gpu',
           '--disable-background-networking', '--no-first-run', '--no-default-browser-check',
           *map(str, args)]
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          text=True, start_new_session=True) as process:
        try:
            stdout, stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            if os.name == 'posix':
                os.killpg(process.pid, signal.SIGKILL)
            else:
                process.kill()
            process.communicate()
            raise RuntimeError('Navegador excedeu o timeout. Confira FORMA_BROWSER e docs/TROUBLESHOOTING.md.')
        result = subprocess.CompletedProcess(cmd, process.returncode, stdout, stderr)
    if result.returncode:
        raise RuntimeError(f'Navegador falhou ({result.returncode}): {result.stderr[-1800:]}')
    return result


def run_audit(path, mode='validate', executable=None):
    """Executa o próprio runtime do HTML em uma cópia isolada, sem outros assets."""
    source = Path(path).resolve().read_text(encoding='utf-8')
    config = json.dumps({'mode': mode})
    script = (TOOLS / 'browser/audit.js').read_text(encoding='utf-8')
    injection = '<script>window.__FORMA_AUDIT__=' + config + ';\n' + script + '</script>'
    if source.lower().count('</body>') != 1:
        raise ValueError('É necessário exatamente um </body> no documento.')
    with tempfile.TemporaryDirectory(prefix='forma-isolated-') as temp:
        isolated = Path(temp) / 'presentation.html'
        isolated.write_text(source.replace('</body>', injection + '\n</body>'), encoding='utf-8')
        result = run_browser(['--virtual-time-budget=20000', '--dump-dom', isolated.as_uri()], executable)
    match = re.search(r'<pre id="forma-audit-result">(.*?)</pre>', result.stdout, re.S)
    if not match:
        raise RuntimeError('O teste JavaScript não terminou. Confira a sintaxe e a API. ' + result.stderr[-1200:])
    report = json.loads(html.unescape(match.group(1)))
    if not report.get('ok'):
        raise RuntimeError(report.get('error', 'Auditoria falhou sem diagnóstico.'))
    return report


def fail_cli(error):
    raise SystemExit(f'ERRO: {error}')
