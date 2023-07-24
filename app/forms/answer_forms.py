from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, IntegerField
from wtforms.validators import DataRequired, Optional
from ..models import TipoQuestao  # Importe a enumeração TipoQuestao da sua aplicação

def numero_to_letra(numero):
    dic = {
        '1': 'A',
        '2': 'B',
        '3': 'C',
        '4': 'D'
    }

    return dic[numero]

class FormularioResposta(FlaskForm):
    submit = SubmitField('Enviar Respostas')

    def __init__(self, questoes, *args, **kwargs):
        self.questoes = questoes
        super(FormularioResposta, self).__init__(*args, **kwargs)

    def process(self, formdata=None, obj=None, data=None, **kwargs):
        for questao in self.questoes:
            if questao.tipo == TipoQuestao.MULTIPLA_ESCOLHA.value:
                unbound_field = RadioField(
                    label=questao.nome,
                    choices=[(numero_to_letra(str(opcao.id)), opcao.texto) for opcao in questao.opcoes],
                    validators=[DataRequired()]
                )
            elif questao.tipo == TipoQuestao.VERDADEIRO_FALSO.value:
                unbound_field = RadioField(
                    label=questao.nome,
                    choices=[('verdadeiro', 'Verdadeiro'), ('falso', 'Falso')],
                    validators=[DataRequired()]
                )
            elif questao.tipo == TipoQuestao.DISCURSIVA.value:
                unbound_field = IntegerField(
                    label=questao.nome,
                    validators=[Optional()]  # Campo discursivo pode ser deixado em branco
                )

            # Bind the UnboundField to this form instance
            bound_field = unbound_field.bind(form=self, name=f'resposta_questao_{questao.id}', prefix=self._prefix)

            # Process the bound field
            bound_field.process(formdata)

            # Set the attribute on the form instance
            setattr(self, f'resposta_questao_{questao.id}', bound_field)

        super(FormularioResposta, self).process(formdata, obj, data, **kwargs)
