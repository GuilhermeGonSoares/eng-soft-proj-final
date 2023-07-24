from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import current_user, login_required
from ..models import *
from ..forms import *
from app import db
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

bp = Blueprint('student', __name__)


def has_student_answered(teste_id, student_matricula):
    # Return True if a CadernoRespostas exists for this teste and student
    return CadernoRespostas.query.filter_by(teste_id=teste_id, aluno_matricula=student_matricula).count() > 0


@bp.route('/testes', methods=['GET'])
@login_required
def index():
    # Fetch all tests
    tests = Teste.query.all()
    # Fetch student's answer notebooks
    notebooks = CadernoRespostas.query.filter_by(aluno_matricula=current_user.matricula).all()
    # Check if the student has answered each test
    has_answered = [has_student_answered(test.id, current_user.matricula) for test in tests]
    return render_template('pages/student.html', tests=tests, notebooks=notebooks, has_answered=has_answered)

@bp.route('/responder_teste/<int:teste_id>', methods=['GET', 'POST'])
@login_required
def answer_test(teste_id):
    teste = Teste.query.get_or_404(teste_id)
    if teste.status != StatusTeste.ABERTO:
        flash("O teste não está aberto para respostas.", category='danger')
        return redirect(url_for('student.index'))

    if request.method == 'GET':

        return render_template('pages/teste.html', teste=teste, questoes=teste.questoes)
    
    if request.method == 'POST':
        cadernoResposta = CadernoRespostas.query.filter_by(teste_id=teste_id, aluno_matricula=current_user.matricula).first()
        if cadernoResposta:
            flash('Está prova só aceita uma tentativa de resposta', category='danger')
            return redirect(url_for('student.index'))

        nota = 0
        cadernoResposta = CadernoRespostas(
            aluno_matricula=current_user.matricula,
            teste_id=teste_id,
            finalizado=True
        )

        db.session.add(cadernoResposta)
        db.session.flush()

        for questao in teste.questoes:
            resposta = Resposta(
                caderno_respostas_id=cadernoResposta.id,
                questao_id=questao.id
            )
            # Obtenha a resposta para esta questão do formulário
            resposta_form = request.form.get(str(questao.id))
            
            resposta.acertou = resposta_form == questao.gabarito
            resposta.resposta = resposta_form
            if resposta.acertou :
                nota += questao.pontuacao

            db.session.add(resposta)
        
        cadernoResposta.nota = nota

        db.session.commit()
        flash('Caderno resposta salvo com sucesso!', 'success')
        return redirect(url_for('student.index'))

@bp.route('/relatorio/<int:teste_id>', methods=['GET', 'POST'])
@login_required
def relatorio_teste(teste_id):
    # Fetch the answer notebook for this test and student
    cadernoResposta = CadernoRespostas.query.filter_by(teste_id=teste_id, aluno_matricula=current_user.matricula).first()

    # If no answer notebook exists, return an error
    if not cadernoResposta:
        flash('Não há respostas para este teste.', category='danger')
        return redirect(url_for('student.index'))
        
    # Fetch the test
    teste = Teste.query.get_or_404(teste_id)
    
    # Fetch the questions for the test
    questoes = teste.questoes

    # Start generating the PDF
    c = canvas.Canvas("relatorios/relatorio.pdf", pagesize=letter)
    width, height = letter

    # Add some custom text
    c.drawString(100, height - 100, f"Relatório de teste para: {current_user.matricula}")
    c.drawString(100, height - 120, f"Nome do teste: {teste.nome}")
    c.drawString(100, height - 140, f"Nota final: {cadernoResposta.nota}")
    
    line_height = 150
    for questao, resposta in zip(questoes, cadernoResposta.respostas):
        line_height += 15
        c.drawString(100, height - line_height, f"Nome da questão: {questao.nome}")
        line_height += 15
        c.drawString(100, height - line_height, f"Enunciado da questão: {questao.texto}")
        line_height += 15
        c.drawString(100, height - line_height, f"Pontuação da questão: {questao.pontuacao}")
        line_height += 15
        c.drawString(100, height - line_height, f"Gabarito da questão: {questao.gabarito}")
        line_height += 15
        c.drawString(100, height - line_height, f"Resposta do aluno: {resposta.resposta}")
        line_height += 15
        c.drawString(100, height - line_height, f"Acertou a questão: {'Sim' if resposta.acertou else 'Não'}")
        line_height += 15

    # Finish up the page and save it
    c.save()

    return send_file('relatorios/relatorio.pdf', as_attachment=True)