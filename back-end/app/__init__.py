from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Flask-SQLalchemy plugin
db = SQLAlchemy()
# Flask-Migrate plugin
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # enable CORS
    CORS(app)
    # init Flask-SQLAlchemy
    db.init_app(app)
    # init Flask-Migrate
    migrate.init_app(app, db)

    #register blueprint 
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix = '/api')

    return app

from app import models