from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, DateTimeLocalField
from wtforms.validators import DataRequired

class TestForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()], render_kw={"placeholder": "Teste Capítulo 5"})
    materia = StringField('Matéria', default='Engenharia de Software', render_kw={"placeholder": "ex. Engenharia de Software", "disabled": True})
    duracao = IntegerField('Duração', validators=[DataRequired()], render_kw={"placeholder": "Duração em Minutos"})
    data = DateTimeLocalField('Data e Hora', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    descricao = TextAreaField('Descrição', render_kw={"placeholder": "Descreva o teste aqui...", "cols": 30, "rows": 5})
    submit = SubmitField('Salvar e Continuar')
