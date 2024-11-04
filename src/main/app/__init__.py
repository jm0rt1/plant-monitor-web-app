from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from .utils.config import ConfigType, config

db = SQLAlchemy()
bootstrap = Bootstrap()


def create_app(config_name: ConfigType) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    bootstrap.init_app(app)  # type:ignore

    # Register blueprints
    from .main.views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
