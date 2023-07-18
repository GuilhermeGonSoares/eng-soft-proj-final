from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from flask import request, abort
from ..models import *
from app import db

bp = Blueprint('teacher', __name__)

@bp.route('/teste', methods=['GET'])
@login_required
def show():
    return render_template('pages/teacher.html')

@bp.route('/teste', methods=['POST'])
@login_required
def create():
    data = request.get_json()
    questions = data['questions']
    nome = data['nomeTeste']
    duracao = data['duracao']

    if len(questions) == 0:
        abort(400, "A lista de perguntas está vazia.")

    teste = Teste(
        nome=nome,
        professor_matricula=current_user.matricula,
        duracao=duracao,
    )

    db.session.add(teste)

    for question in questions:
        tipo = question['tipo']
        enunciado = question['enunciado']
        pontuacao = question['pontuacao']

        nova_questao = Questao(
            tipo=tipo,
            pontuacao=pontuacao,  # Substitua com a pontuação real da questão
            texto=enunciado,
            gabarito=question['resposta'],
            teste=teste,
        )
        if tipo == 'multipla_escolha':
            alternativas = question['alternativas']
            print(question['resposta'])
            choices = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
            for i, alternativa in enumerate(alternativas):
                opcao = Opcao(
                    questao=nova_questao,
                    texto=alternativa,
                    eh_correta=(choices[i] == question['resposta']),
                    letra=choices[i]
                )
                db.session.add(opcao)

        db.session.add(nova_questao)

    db.session.commit()

    return redirect(url_for('teacher.show'))