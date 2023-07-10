from app import db, login_manager
from flask import render_template, redirect, url_for, flash, Blueprint, request
from ..forms import LoginForm, RegisterForm
from ..models import User, MatriculaProfessor
from ..utils.professor_required_decorator import professor_required
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime

bp = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(matricula):
    return User.query.get(matricula)


@login_manager.unauthorized_handler
def unauthorized():
    # Redireciona o usuário para a página de login
    return redirect(url_for("auth.login"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            attempted_user = User.query.filter_by(matricula=form.matricula.data).first()
            if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.senha.data
            ):
                login_user(attempted_user)
                flash(
                    f"Sucesso! Seja bem-vindo {attempted_user.email} - {attempted_user.matricula}",
                    category="success",
                )
                if attempted_user.eh_professor:
                    return redirect(url_for("teacher.show"))
                else:
                    return redirect(url_for("student.home"))

            else:
                flash(
                    "Matrícula e senha não batem! Por favor, tente novamente",
                    category="danger",
                )
    return render_template("pages/login.html", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            matricula = form.matricula.data
            funcao = form.funcao.data
            user = User(
                matricula=matricula,
                email=form.email.data,
                senha=form.senha.data,
                nome=form.nome.data,
                eh_professor=False,
            )

            if funcao == "teacher":
                matricula_professor = MatriculaProfessor.query.filter_by(
                    matricula=matricula
                ).first()
                if not matricula_professor:
                    flash("Matrícula de professor inválida.", category="danger")
                    return render_template("pages/register.html", form=form)
                else:
                    user.eh_professor = True

            db.session.add(user)
            db.session.commit()

            return redirect(url_for("auth.login"))

        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(
                    f"{err_msg[0]}",
                    category="danger",
                )
    return render_template("pages/register.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))