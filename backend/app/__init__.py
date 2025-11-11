import logging
from flask import Flask
from flask_cors import CORS
from .config.settings import Config
from .database.setup import db
from flask_migrate import Migrate

def create_app() -> Flask:
    """Фабрика приложения Flask"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, app.config.get('LOG_LEVEL', 'INFO')),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    db.init_app(app)
    CORS(app)

    Migrate(app, db)

    from .api.routes import api
    app.register_blueprint(api, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app

