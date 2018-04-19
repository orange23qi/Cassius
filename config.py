import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    COMPANY_NAME = 'ezbuy'
    GITHUB_URL = 'http://gitlab.1dmy.com'
    PRIVATE_TOKEN = 'm-_z7wngsMAx-oi_T5q2'

    SECRET_KEY = "hfusaf2m4ot#7)fkw#di2bu6(cv0@opwmafx5n#6=3d%x^hpl6"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    #SQLALCHEMY_ECHO = True

    CONFIG_DB_USER = 'chenqi'
    CONFIG_DB_PASSWORD = 'chenqi'
    CONFIG_DB_HOST = '192.168.199.134'
    CONFIG_DB_PORT = '3306'
    CONFIG_DB_SCHEMA = 'test'

    BETA_DB_USER = 'chenqi'
    BETA_DB_PASSWORD = 'chenqi'
    BETA_DB_HOST = '192.168.199.134'
    BETA_DB_PORT = '3306'

    PARSE_DB_USER = 'chenqi'
    PARSE_DB_PASSWORD = 'chenqi'
    PARSE_DB_HOST = '192.168.199.134'
    PARSE_DB_PORT = '3306'
    PARSE_DB_SCHEMA = 'sqlparse'

    INCEPTION_HOST = '192.168.199.134'
    INCEPTION_PORT = '6669'

    INCEPTION_REMOTE_BACKUP_HOST = ''
    INCEPTION_REMOTE_BACKUP_PORT = ''
    INCEPTION_REMOTE_BACKUP_USER = ''
    INCEPTION_REMOTE_BACKUP_PASSWORD = ''

    REDIS_HOST = '192.168.199.134'
    REDIS_PORT = '7000'
    REDIS_DB = '0'

    SQLALCHEMY_DATABASE_URI = 'mysql://' + CONFIG_DB_USER + ':' \
        + CONFIG_DB_PASSWORD + '@' + CONFIG_DB_HOST + ':' \
        + CONFIG_DB_PORT + '/' + CONFIG_DB_SCHEMA


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = ''


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = ''


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
