def test_init_db(runner, monkeypatch):
    class Recorder(object):
        called = False
    
    def fake_init_db():
        Recorder.called = True
    
    monkeypatch.setattr('demo.db.create_all', fake_init_db)
    rv = runner.invoke(args=['init-db'])

    assert 'Intialize' in rv.output
    assert Recorder.called

def test_create_all(db):
    from sqlalchemy import inspect
    db.create_all()
    for table in db.Model.metadata.sorted_tables:
        assert inspect(db.engine).has_table(table.key)
    
def test_drop_all(db):
    from sqlalchemy import inspect
    db.drop_all()
    for table in db.Model.metadata.sorted_tables:
        assert not inspect(db.engine).has_table(table.key)
