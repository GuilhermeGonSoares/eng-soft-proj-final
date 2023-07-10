from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, ValidationError, Regexp
from app.models import User


class RegisterForm(FlaskForm):
    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()

        if user:
            raise ValidationError("Email já cadastrado")

    def validate_matricula(self, matricula_to_check):
        user = User.query.filter_by(matricula=matricula_to_check.data).first()

        if user:
            raise ValidationError("Matricula já cadastrado")

    matricula = StringField(
        label="Matrícula *",
        validators=[
            DataRequired(),
            Length(min=9, max=9, message="A matrícula deve ter 9 caracteres."),
        ],
        render_kw={"class": "input-field", "placeholder": "Digite a matrícula"}
    )
    nome = StringField(label="Nome *", validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField(
        label="Email *",
        validators=[
            DataRequired(),
            Regexp(
                r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                message="Email inválido",
            ),
        ],
        render_kw={"class": "input-field", "placeholder": "Digite o email"}
    )
    senha = PasswordField(
        label="Senha *",
        validators=[
            DataRequired(),
            Length(min=4, message="A senha tem que ter no mínimo 4 caracteres"),
        ],
        render_kw={"class": "input-field", "placeholder": "Digite a senha"}
    )
    funcao = RadioField(
        label="Você é?",
        choices=[("student", "I'm a student and want to increase my performance"),
                ("teacher", "I'm a teacher and want to manage my essays")],
        default="student",
        render_kw={"class": "radio-input"}
    )
    submit = SubmitField(label="Fazer Cadastro")


class LoginForm(FlaskForm):
    matricula = StringField(
        label="Matrícula",
        validators=[
            DataRequired(),
            Length(min=9, max=9, message="A matrícula deve ter 9 caracteres."),
        ],
        render_kw={"class": "input-field", "placeholder": "Digite a matrícula"}
    )
    senha = PasswordField(
        label="Senha",
        validators=[
            DataRequired(),
            Length(min=4, message="A senha tem que ter no mínimo 4 caracteres"),
        ],
        render_kw={"class": "input-field", "placeholder": "Digite a senha"}
    )
    submit = SubmitField(label="Login")