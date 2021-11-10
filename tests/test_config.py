import os
import tempfile

def run_command(cmd):
    fid, fpath = tempfile.mkstemp()
    os.system(f'{cmd} > {fpath} 2>&1')
    rv = open(fpath).read()
    os.close(fid)
    os.unlink(fpath)
    return rv

def test_dev_config(env, monkeypatch):
    monkeypatch.setenv('FLASK_ENV', 'development')
    rv = run_command('timeout 2 flask run')
    assert 'Environment: development' in rv

def test_test_config(env, monkeypatch):
    monkeypatch.setenv('FLASK_ENV', 'test')
    rv = run_command('timeout 2 flask run')
    assert 'Environment: test' in rv
