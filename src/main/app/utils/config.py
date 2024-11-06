from enum import Enum
import os
from pathlib import Path

basedir = Path("instance").resolve()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'data-dev.db')
    )


class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'test-dev.db')
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
    test = 'test'


config: dict[ConfigType, type[Config]] = {
    ConfigType.development: DevelopmentConfig,
    ConfigType.production: ProductionConfig,
    ConfigType.default: DevelopmentConfig,
    ConfigType.test: TestConfig

}
