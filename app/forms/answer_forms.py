from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, BooleanField, TextAreaField, FieldList, FormField
from wtforms.validators import DataRequired

class MultiplaEscolhaForm(FlaskForm):
    opcao = RadioField('Opções', coerce=int)

class VerdadeiroFalsoForm(FlaskForm):
    opcao = BooleanField('Verdadeiro ou Falso?')

class DiscursivaForm(FlaskForm):
    resposta = TextAreaField('Resposta')



class TesteForm(FlaskForm):
    multipla_escolha = FieldList(FormField(MultiplaEscolhaForm), min_entries=0)
    verdadeiro_falso = FieldList(FormField(VerdadeiroFalsoForm), min_entries=0)
    discursiva = FieldList(FormField(DiscursivaForm), min_entries=0)
    submit = SubmitField('Submit')
