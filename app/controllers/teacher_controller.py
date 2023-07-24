from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from flask import request, abort
from ..models import *
from ..forms import TestForm
from app import db

bp = Blueprint('teacher', __name__)

@bp.route('/teste', methods=['GET'])
@login_required
def show():
    testes = Teste.query.all()
    return render_template(
        'pages/teacher.html',
        testes=testes)


@bp.route('/teste/<int:teste_id>/questions', methods=['GET', 'POST'])
@login_required
def create_questions(teste_id):
    if request.method == 'GET':
        return render_template('pages/building.html', teste_id=teste_id)
    
    elif request.method == 'POST':
        questions = request.get_json()
        print(questions)
        
        current_test = Teste.query.get(teste_id)
        nota = 0
        # Loop through all questions
        for questionData in questions:
            # Create a new question object
            nota += questionData['score']
            newQuestion = Questao(
                nome=questionData['name'],
                teste_id=teste_id,
                tipo=questionData['type'],
                pontuacao=questionData['score'],
                texto=questionData['description'],
                gabarito=None  # We'll fill this in later
            )

            # Add the new question to the database session
            db.session.add(newQuestion)
            db.session.flush()  # Use flush to ensure the new question ID is generated

            # If the question type is multiple choice, create the options and set the correct answer
            if questionData['type'] == 'multipla_escolha':
                for alternativeData in questionData['alternatives']:
                    newOption = Opcao(
                        questao_id=newQuestion.id,
                        texto=alternativeData['content'],
                        eh_correta=alternativeData['isCorrect']
                    )

                    # If this option is the correct one, set it as the answer key
                    if alternativeData['isCorrect']:
                        newQuestion.gabarito = newOption.texto

                    # Add the new option to the database session
                    db.session.add(newOption)
            else:
                newQuestion.gabarito = questionData['answer']
        current_test.nota = nota
        # Commit the database session to save all new questions and options
        db.session.commit()

        # Redirect the user to the "teacher.show" page
        return redirect(url_for('teacher.show'))



@bp.route('/teste/', methods=['GET', 'POST'])
@login_required
def create_test():
    form = TestForm()
    if form.validate_on_submit():
        teste = Teste(
            nome=form.nome.data,
            professor_matricula=current_user.matricula,
            nota=0,  
            duracao=form.duracao.data,
            abertura=form.data.data,
            descricao=form.descricao.data,
        )
        
        db.session.add(teste)
        db.session.commit()
        return redirect(url_for('teacher.create_questions', teste_id=teste.id))  

    return render_template('pages/configTeste.html', form=form, step=1)


@bp.route('/delete_test/<int:teste_id>', methods=['GET'])
@login_required
def delete_test(teste_id):
    teste = Teste.query.filter_by(id=teste_id).first()
    
    if teste:
        db.session.delete(teste)
        db.session.commit()

    return redirect(url_for('teacher.show'))

@bp.route('/change_test_status/<int:teste_id>/<string:new_status>', methods=['GET'])
@login_required
def change_test_status(teste_id, new_status):
    teste = Teste.query.get_or_404(teste_id)
    if teste:
        if new_status.upper() in StatusTeste.__members__:
            teste.status = StatusTeste[new_status.upper()]
            db.session.commit()
    return redirect(url_for('teacher.show'))



# @bp.route('/teste', methods=['GET', 'POST'])
# @login_required
# def create():
#     data = request.get_json()
#     questions = data['questions']
#     nome = data['nomeTeste']
#     duracao = data['duracao']

#     if len(questions) == 0:
#         abort(400, "A lista de perguntas está vazia.")

#     teste = Teste(
#         nome=nome,
#         professor_matricula=current_user.matricula,
#         duracao=duracao,
#     )

#     db.session.add(teste)

#     for question in questions:
#         tipo = question['tipo']
#         enunciado = question['enunciado']
#         pontuacao = question['pontuacao']

#         nova_questao = Questao(
#             tipo=tipo,
#             pontuacao=pontuacao,  # Substitua com a pontuação real da questão
#             texto=enunciado,
#             gabarito=question['resposta'],
#             teste=teste,
#         )
#         if tipo == 'multipla_escolha':
#             alternativas = question['alternativas']
#             print(question['resposta'])
#             choices = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
#             for i, alternativa in enumerate(alternativas):
#                 opcao = Opcao(
#                     questao=nova_questao,
#                     texto=alternativa,
#                     eh_correta=(choices[i] == question['resposta']),
#                     letra=choices[i]
#                 )
#                 db.session.add(opcao)

#         db.session.add(nova_questao)

#     db.session.commit()

#     return redirect(url_for('teacher.show'))