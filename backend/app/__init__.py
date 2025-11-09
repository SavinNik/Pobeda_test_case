from flask import Flask
from flask_cors import CORS
from backend.app.config.settings import Config
from backend.app.database.setup import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app)

    from backend.app.api.routes import api
    app.register_blueprint(api, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app

