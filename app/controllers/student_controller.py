from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from datetime import datetime, timedelta
from ..models import *
from ..forms import *
from app import db
from sqlalchemy import or_

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
    teste = Teste.query.get(teste_id)
    if not teste:
        return "Teste não encontrado", 404

    if teste.status != StatusTeste.ABERTO:
        return "Teste não está aberto", 403

    caderno_respostas = CadernoRespostas.query.filter_by(teste_id=teste_id, aluno_matricula=current_user.matricula).first()
    if not caderno_respostas:
        caderno_respostas = CadernoRespostas(teste_id=teste_id, aluno_matricula=current_user.matricula)
        db.session.add(caderno_respostas)
        db.session.commit()

    form = TesteForm()
    for i, questao in enumerate(teste.questoes):
        if questao.tipo == TipoQuestao.MULTIPLA_ESCOLHA:
            form.multipla_escolha.append_entry()
            form.multipla_escolha[i].opcao.choices = [(opcao.id, opcao.texto) for opcao in questao.opcoes]
        elif questao.tipo == TipoQuestao.VERDADEIRO_FALSO:
            form.verdadeiro_falso.append_entry()
        elif questao.tipo == TipoQuestao.DISCURSIVA:
            form.discursiva.append_entry()

    if form.validate_on_submit():
        for i, questao in enumerate(teste.questoes):
            if questao.tipo == TipoQuestao.MULTIPLA_ESCOLHA:
                resposta = Resposta(caderno_respostas_id=caderno_respostas.id, questao_id=questao.id, resposta=form.multipla_escolha[i].opcao.data, acertou=form.multipla_escolha[i].opcao.data == questao.gabarito)
            elif questao.tipo == TipoQuestao.VERDADEIRO_FALSO:
                resposta = Resposta(caderno_respostas_id=caderno_respostas.id, questao_id=questao.id, resposta=form.verdadeiro_falso[i].opcao.data, acertou=form.verdadeiro_falso[i].opcao.data == questao.gabarito)
            elif questao.tipo == TipoQuestao.DISCURSIVA:
                resposta = Resposta(caderno_respostas_id=caderno_respostas.id, questao_id=questao.id, resposta=form.discursiva[i].resposta.data)
            db.session.add(resposta)
        db.session.commit()
        return redirect(url_for('testes'))
        
    return render_template('pages/answer_test.html', form=form, questoes=teste.questoes)



# choices_ans = {
#     '1': 'A',
#     '2': 'B',
#     '3': 'C',
#     '4': 'D'
# }

# def formatar_tempo_restante(tempo_restante):
#     segundos_totais = tempo_restante.total_seconds()
#     horas = int(segundos_totais // 3600)
#     minutos = int((segundos_totais % 3600) // 60)
#     segundos = int(segundos_totais % 60)
#     return f"{horas:02d}:{minutos:02d}:{segundos:02d}"


# def descrever_teste(testes_disponiveis):
#     testes_info = []
#     now = datetime.utcnow()
    
#     for teste in testes_disponiveis:
#         questoes_count = len(teste.questoes)
        
#         tempo_restante = None
#         if teste.created_at:
#             duracao = timedelta(minutes=teste.duracao)
#             tempo_final = teste.created_at + duracao
#             tempo_restante = tempo_final - now
        
#         teste_info = {
#             'teste': teste,
#             'questoes_count': questoes_count,
#             'tempo_restante': formatar_tempo_restante(tempo_restante),
#         }
        
#         testes_info.append(teste_info)

#     return testes_info


# @bp.route('/prova')
# @login_required
# def index():
#     testes = Teste.query.all()
#     testes_disponiveis = []
#     testes_concluidos = []

#     for teste in testes:
#         caderno_resposta = CadernoRespostas.query.filter_by(
#             aluno_matricula=current_user.matricula,
#             teste_id=teste.id
#             ).first()
#         nota = 0
#         if caderno_resposta:
#             nota = caderno_resposta.nota
#         if teste.ativo == False:
#             testes_concluidos.append((teste, nota))
#         else:
#             if caderno_resposta and caderno_resposta.finalizado:
#                 testes_concluidos.append((teste, nota))
#             else:
#                 testes_disponiveis.append(teste)
    
#     testes_info = descrever_teste(testes_disponiveis)
    
#     return render_template('pages/student.html', 
#                            testes_info=testes_info,
#                            testes_info_concluidos=testes_concluidos
#                            )


# @bp.route('/prova/<int:teste_id>/questao/<int:questao_id>', methods=['GET', 'POST'])
# @login_required
# def show(teste_id, questao_id):
#     matricula = current_user.matricula
    
#     caderno_respostas = CadernoRespostas.query.filter_by(aluno_matricula=matricula, teste_id=teste_id).first()
#     print(caderno_respostas)
#     if not caderno_respostas:
#         caderno_respostas = CadernoRespostas(aluno_matricula=matricula, teste_id=teste_id)
#         db.session.add(caderno_respostas)
#         db.session.commit()
    
#     resposta = Resposta.query.filter_by(
#             caderno_respostas=caderno_respostas,
#             questao_id=questao_id
#         ).first()

#     if request.method == 'POST':
#         alternativa_selecionada = request.form.get('options')
#         print('alternativa_selecionada', alternativa_selecionada)
#         questao = Questao.query.get(questao_id)
        
#         if not resposta:
#             nova_resposta = Resposta(
#                 caderno_respostas=caderno_respostas,
#                 questao_id=questao_id,
#                 resposta=alternativa_selecionada,
#                 acertou = alternativa_selecionada == questao.gabarito
#             )
#             db.session.add(nova_resposta)
#             db.session.commit()
#         else:
#             atualizar_resposta = resposta
#             atualizar_resposta.resposta = alternativa_selecionada
#             atualizar_resposta.acertou = alternativa_selecionada == questao.gabarito
#             db.session.add(atualizar_resposta)
#             db.session.commit()
        
#         if request.form.get('action') == 'finalizar':
#             todas_respostas = Resposta.query.filter_by(caderno_respostas=caderno_respostas).all()
#             nota = 0
#             for res in todas_respostas:
#                 if res.acertou:
#                     nota += int(res.questao.pontuacao)
            
#             caderno_respostas.finalizado = True
#             caderno_respostas.nota = nota
#             db.session.add(caderno_respostas)
#             db.session.commit()
#             return redirect(url_for('student.index'))

#         return redirect(url_for('student.show', teste_id=teste_id, questao_id=questao_id + 1))

#     else:
        
#         teste = Teste.query.get(teste_id)
#         test_info = descrever_teste([teste])[0]
#         questao = next(filter(lambda q: q.id == questao_id, teste.questoes), None)
#         questao_anterior =  next(filter(lambda q: q.id == questao_id - 1, teste.questoes), None)
#         proxima_questao =  next(filter(lambda q: q.id == questao_id + 1, teste.questoes), None)
#         questao_number = teste.questoes.index(questao)
        
        
#         return render_template('pages/exame.html', 
#                             test_info = test_info, 
#                             questao=questao, 
#                             questao_anterior=questao_anterior,
#                             proxima_questao=proxima_questao,
#                             questao_number=questao_number + 1,
#                             resposta=resposta.resposta if resposta else None
#                             )

