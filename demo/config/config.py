class Config(object):
    """ Base configuration file. """
    ### FLASK ###
    NAME = 'demo'
    DESCRIPTION = '<description-here>'
    VERSION = '1.0'

    DEBUG = False
    TESTING = False
    PORT  = 5000
    HOST  = 'localhost'

    WORKER = 4

    ### API KEYS ###
    OWM_API_KEY = None # define using export OWM_API_KEY XXX
    SOL_API_KEY = None # define using export OWM_API_KEY XXX

    ### JWT ###
    JWT_ALGORITHM = 'RS256'
    JWT_SECRET_KEY_PATH = 'secret-key.pem'
    @property
    def JWT_SECRET_KEY(self):
        """ data in `JWT_SECRET_KEY_PATH` """
        try:
            return open(self.JWT_SECRET_KEY_PATH, 'rb').read()
        except FileNotFoundError:
            return None

    ### DATABASE ###
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQL_USERNAME = 'user0'
    SQL_PASSWORD = 'secret'
    SQL_HOST = 'localhost'
    SQL_DATABASE = 'demo'
    @property
    def  SQLALCHEMY_DATABASE_URI(self):
        """
        `mysql+pymysql://`**`SQL_USERNAME`**`:`**`SQL_PASSWORD`**`@`**`SQL_HOST`**`/`**`SQL_DATABASE`**
        """
        return ('mysql+pymysql://'
                f'{self.SQL_USERNAME}:'
                f'{self.SQL_PASSWORD}'
                f'@{self.SQL_HOST}'
                f'/{self.SQL_DATABASE}')

    ### CELERY ###
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_result_backend = 'redis://localhost:6379/0'

class developmentConfig(Config):
    """ Configuration for `developement` environment. """
    DEBUG = True
    HOST  = '0.0.0.0'
    PORT  = 8080

class testConfig(Config):
    """ Configuration for `test` environment. """
    TESTING = True
    SQL_DATABASE = 'demo_test'