from flask import Blueprint, render_template, redirect, url_for, make_response
from flask_login import current_user, login_required
from flask import request, abort
from ..models import *
from ..forms import TestForm
from app import db
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from io import BytesIO


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


@bp.route('/listar_alunos/<int:teste_id>', methods=['GET'])
@login_required
def listar_alunos(teste_id):
    alunos = User.query.filter_by(eh_professor=False).all() 
    teste = Teste.query.get_or_404(teste_id)
    cadernos_resposta_teste = []

    for aluno in alunos:
        caderno_resposta = CadernoRespostas.query.filter_by(aluno_matricula=aluno.matricula, teste_id=teste_id).first()
        
        cadernos_resposta_teste.append((aluno, caderno_resposta))


    return render_template('pages/listar_alunos.html', cadernos_resposta=cadernos_resposta_teste, teste=teste)



@bp.route('/relatorio/teste/<int:teste_id>/aluno/<string:matricula>', methods=['GET'])
@login_required
def relatorio(teste_id, matricula):
    # Buscar teste
    teste = Teste.query.get(teste_id)

    # Buscar caderno de respostas
    caderno_respostas = CadernoRespostas.query.filter_by(teste_id=teste_id, aluno_matricula=matricula).first()

    # Cria o documento PDF
    buff = BytesIO()
    doc = SimpleDocTemplate(buff, pagesize=landscape(letter))
    elements = []

    # Cabeçalho do relatório
    elements.append(Paragraph(f"Relatório do teste {teste.nome}", getSampleStyleSheet()["Heading1"]))

    # Tabela com as questões e respostas
    data = [['Questão', 'Resposta do aluno', 'Gabarito', 'Acertou', 'Pontuação']]

    for resposta in caderno_respostas.respostas:
        questao = resposta.questao
        acertou = 'Sim' if resposta.acertou else 'Não'
        data.append([questao.nome, resposta.resposta, questao.gabarito, acertou, questao.pontuacao])

    table = Table(data)
    elements.append(table)

    # Adiciona a nota final
    elements.append(Paragraph(f"Nota final: {caderno_respostas.nota}", getSampleStyleSheet()["Normal"]))

    doc.build(elements)

    # Envia a resposta com o arquivo PDF
    response = make_response(buff.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=relatorio_teste_{teste.nome}_aluno_{matricula}.pdf'
    return response