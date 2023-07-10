from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from .config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from . import models

    with app.app_context():
        db.create_all()

    from .controllers import blueprints

    for bp in blueprints():
        app.register_blueprint(bp, url_prefix=f"/{bp.name}")
    
    return app 


