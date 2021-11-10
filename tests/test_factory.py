import os

def test_env(app):
    rv = app.testing
    assert rv

def test_name_and_version(app):
    from demo import config
    # test name
    rv = app.config['NAME']
    assert rv == config.NAME
    # test version
    rv = app.config['VERSION']
    assert rv == config.VERSION

def test_connection(client):
    resp = client.get('/ok')
    assert resp.data == b'OK'