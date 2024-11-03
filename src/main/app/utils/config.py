from enum import Enum
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'data-dev.db')
    )


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'data.db')
    )


class ConfigType(str, Enum):
    development = 'development'
    production = 'production'
    default = 'default'


config: dict[ConfigType, type[Config]] = {
    ConfigType.development: DevelopmentConfig,
    ConfigType.production: ProductionConfig,
    ConfigType.default: DevelopmentConfig
}
