from demo import config
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import click

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))
Model = declarative_base()
Model.query = session.query_property()

@click.command('init-db')
def init_db():
    drop_all()
    create_all()
    click.echo(f'Intialize Database ({config.SQL_DATABASE})')

def create_all():
    """Create all tables defined in `demo.models`."""
    import demo.models
    Model.metadata.create_all(bind=engine)

def drop_all():
    """Delete all tables defined in `demo.models`."""
    import demo.models
    Model.metadata.drop_all(bind=engine)
