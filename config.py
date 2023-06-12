# config.py

class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:longacre@localhost:3306/expenses_dev'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:longacre@localhost:3306/expenses_test'


class ProductionConfig(Config):
    pass
