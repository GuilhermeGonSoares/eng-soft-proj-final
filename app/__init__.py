from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler

from .config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def seed():
    from .models.user import MatriculaProfessor
    matriculas = ["999999999", "888888888", "777777777"]

    for matricula in matriculas:
        matricula_exist = MatriculaProfessor.query.filter_by(matricula=matricula).first()
        if not matricula_exist:
            professor = MatriculaProfessor(matricula=matricula)
            db.session.add(professor)

    db.session.commit()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .models.exame import fechar_testes, abrir_testes
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=fechar_testes, trigger="interval", minutes=1)
    scheduler.add_job(func=abrir_testes, trigger="interval", minutes=1)
    scheduler.start()

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()
        seed()

    from .controllers import blueprints

    for bp in blueprints():
        app.register_blueprint(bp, url_prefix=f"/{bp.name}")
    
    return app 


app = create_app()


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("auth.login"))
