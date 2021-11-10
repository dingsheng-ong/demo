from demo import config, db
from flask import Flask
import logging
import os

logging.basicConfig(level=logging.DEBUG,
                    # format=f'[%(asctime)s]: {os.getpid()} %(levelname)s %(message)s',
                    # datefmt='%Y-%m-%d %H:%M:%S',
                    format=f'[%(levelname)s] %(message)s',
                    handlers=[logging.StreamHandler()])
logger = logging.getLogger()

def create_app():
    """
    Flask application factory function.

    Returns:
        `Flask`: Flask app
    """
    app = Flask(config.NAME)
    app.config.from_object(config)

    # database
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        logger.info('Shutting down database.')
        db.session.remove()
    app.cli.add_command(db.init_db)

    # blueprints
    from demo.views import auth
    app.register_blueprint(auth)

    # connection test
    @app.route('/ok')
    def ok():
        return f'OK'

    logger.info(f' App: {config.NAME} v{config.VERSION}')
    logger.info(f'Mode: {config.FLASK_ENV}')

    return app
