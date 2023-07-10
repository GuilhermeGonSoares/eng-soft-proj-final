from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from datetime import datetime, timedelta
from ..models import Teste, Questao, User, Resposta, CadernoRespostas
from app import db
from sqlalchemy import or_

bp = Blueprint('student', __name__)

choices_ans = {
    '1': 'A',
    '2': 'B',
    '3': 'C',
    '4': 'D'
}

def formatar_tempo_restante(tempo_restante):
    segundos_totais = tempo_restante.total_seconds()
    horas = int(segundos_totais // 3600)
    minutos = int((segundos_totais % 3600) // 60)
    segundos = int(segundos_totais % 60)
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"


def descrever_teste(testes_disponiveis):
    testes_info = []
    now = datetime.utcnow()
    
    for teste in testes_disponiveis:
        questoes_count = len(teste.questoes)
        
        tempo_restante = None
        if teste.created_at:
            duracao = timedelta(minutes=teste.duracao)
            tempo_final = teste.created_at + duracao
            tempo_restante = tempo_final - now
        
        teste_info = {
            'teste': teste,
            'questoes_count': questoes_count,
            'tempo_restante': formatar_tempo_restante(tempo_restante),
        }
        
        testes_info.append(teste_info)

    return testes_info


@bp.route('/prova')
def index():
    testes_ativos = Teste.query.filter_by(ativo=True).all()
    testes_disponiveis = []
    testes_concluidos = []
    print(testes_ativos)
    for teste in testes_ativos:
        if len(teste.caderno_respostas) == 0:
            print(teste)
            testes_disponiveis.append(teste)
        else:
            print(teste.caderno_respostas)
            achou = False
            for caderno_resposta in teste.caderno_respostas:
                if caderno_resposta.aluno_matricula == current_user.matricula:
                    achou = True
                    if caderno_resposta.finalizado == False:
                        testes_disponiveis.append(teste)
                    else:
                        testes_concluidos.append((teste, caderno_resposta.nota))
                    break
            if achou == False:
                testes_disponiveis.append(teste)
    

    
    testes_info = descrever_teste(testes_disponiveis)
    
    return render_template('pages/student.html', 
                           testes_info=testes_info,
                           testes_info_concluidos=testes_concluidos
                           )


@bp.route('/prova/<int:teste_id>/questao/<int:questao_id>', methods=['GET', 'POST'])
def show(teste_id, questao_id):
    matricula = current_user.matricula
    
    caderno_respostas = CadernoRespostas.query.filter_by(aluno_matricula=matricula, teste_id=teste_id).first()
    print(caderno_respostas)
    if not caderno_respostas:
        caderno_respostas = CadernoRespostas(aluno_matricula=matricula, teste_id=teste_id)
        db.session.add(caderno_respostas)
        db.session.commit()
    
    resposta = Resposta.query.filter_by(
            caderno_respostas=caderno_respostas,
            questao_id=questao_id
        ).first()

    if request.method == 'POST':
        alternativa_selecionada = request.form.get('options')
        print('alternativa_selecionada', alternativa_selecionada)
        questao = Questao.query.get(questao_id)
        
        if not resposta:
            nova_resposta = Resposta(
                caderno_respostas=caderno_respostas,
                questao_id=questao_id,
                resposta=alternativa_selecionada,
                acertou = alternativa_selecionada == questao.gabarito
            )
            db.session.add(nova_resposta)
            db.session.commit()
        else:
            atualizar_resposta = resposta
            atualizar_resposta.resposta = alternativa_selecionada
            atualizar_resposta.acertou = alternativa_selecionada == questao.gabarito
            db.session.add(atualizar_resposta)
            db.session.commit()
        
        if request.form.get('action') == 'finalizar':
            todas_respostas = Resposta.query.filter_by(caderno_respostas=caderno_respostas).all()
            nota = 0
            for res in todas_respostas:
                if res.acertou:
                    nota += res.questao.pontuacao
            
            caderno_respostas.finalizado = True
            caderno_respostas.nota = nota
            db.session.add(caderno_respostas)
            db.session.commit()
            return redirect(url_for('student.index'))

        return redirect(url_for('student.show', teste_id=teste_id, questao_id=questao_id + 1))

    else:
        
        teste = Teste.query.get(teste_id)
        test_info = descrever_teste([teste])[0]
        questao = next(filter(lambda q: q.id == questao_id, teste.questoes), None)
        questao_anterior =  next(filter(lambda q: q.id == questao_id - 1, teste.questoes), None)
        proxima_questao =  next(filter(lambda q: q.id == questao_id + 1, teste.questoes), None)
        questao_number = teste.questoes.index(questao)
        
        
        return render_template('pages/exame.html', 
                            test_info = test_info, 
                            questao=questao, 
                            questao_anterior=questao_anterior,
                            proxima_questao=proxima_questao,
                            questao_number=questao_number + 1,
                            resposta=resposta.resposta if resposta else None
                            )

