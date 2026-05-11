import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[3]


def find_free_port():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_instance:
    socket_instance.bind(('127.0.0.1', 0))
    return socket_instance.getsockname()[1]


def wait_for_server(base_url, process, timeout=10):
  deadline = time.time() + timeout
  last_error = None

  while time.time() < deadline:
    if process.poll() is not None:
      output = process.stdout.read() if process.stdout else ''
      raise RuntimeError(f'Flask server stopped early:\n{output}')

    try:
      with urlopen(base_url, timeout=0.5) as response:
        if response.status < 500:
          return
    except (URLError, TimeoutError, ConnectionError) as error:
      last_error = error
      time.sleep(0.2)

  raise RuntimeError(f'Flask server did not start in time. Last error: {last_error}')


def run_migrations(env):
  subprocess.run(
    [sys.executable, '-m', 'flask', '--app', 'run:app', 'db', 'upgrade'],
    cwd=PROJECT_ROOT,
    env=env,
    check=True,
  )


@pytest.fixture(scope='session')
def e2e_base_url(tmp_path_factory):
  db_path = tmp_path_factory.mktemp('e2e_db') / 'journal_e2e.sqlite'
  port = find_free_port()

  env = os.environ.copy()
  env.update(
    {
      'DATABASE_URL': f'sqlite:///{db_path}',
      'SECRET_KEY': 'e2e-test-secret-key',
      'HOST': '127.0.0.1',
      'PORT': str(port),
      'FLASK_DEBUG': '0',
    }
  )

  run_migrations(env)

  process = subprocess.Popen(
    [sys.executable, 'run.py'],
    cwd=PROJECT_ROOT,
    env=env,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
  )

  base_url = f'http://127.0.0.1:{port}'

  try:
    wait_for_server(base_url, process)
    yield base_url
  finally:
    process.terminate()
    try:
      process.wait(timeout=5)
    except subprocess.TimeoutExpired:
      process.kill()
