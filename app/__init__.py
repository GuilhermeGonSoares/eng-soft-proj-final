from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler

from .config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .models.exame import fechar_testes

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=fechar_testes, trigger="interval", minutes=1)
    scheduler.start()

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from .controllers import blueprints

    for bp in blueprints():
        app.register_blueprint(bp, url_prefix=f"/{bp.name}")
    
    return app 


app = create_app()
