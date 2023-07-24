from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import current_user, login_required
from ..models import *
from ..forms import *
from app import db
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO

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

@bp.route('/relatorio/<int:teste_id>', methods=['GET'])
@login_required
def relatorio_teste(teste_id):
    cadernoResposta = CadernoRespostas.query.filter_by(teste_id=teste_id, aluno_matricula=current_user.matricula).first()
    respostas = cadernoResposta.respostas
    teste = Teste.query.get_or_404(teste_id)
    # Cria o documento PDF
    buff = BytesIO()
    doc = SimpleDocTemplate(buff, pagesize=landscape(letter))
    style = getSampleStyleSheet()
    data = [['Nome da questão', 'Pontuação da questão', 'Gabarito', 'Resposta do aluno', 'Correto?']]
    aluno = []
    for resposta in respostas:
        aluno.append(resposta.caderno_respostas.aluno)
        questao = resposta.questao
        correto = 'Correto' if resposta.acertou else 'Incorreto'
        
        data.append([questao.nome, questao.pontuacao, questao.gabarito, resposta.resposta, correto])
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ]))
    elements = []
    elements.append(table)
    doc.build(elements)

    # Envia a resposta com o arquivo PDF
    response = make_response(buff.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=relatorio_{teste.nome}_{aluno[0].matricula}.pdf'
    return response
   