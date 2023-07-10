from flask import Blueprint, render_template
from datetime import datetime, timedelta
from ..models import Teste, Questao

bp = Blueprint('student', __name__)

def formatar_tempo_restante(tempo_restante):
    segundos_totais = tempo_restante.total_seconds()
    horas = int(segundos_totais // 3600)
    minutos = int((segundos_totais % 3600) // 60)
    segundos = int(segundos_totais % 60)
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"


@bp.route('/prova')
def index():
    testes_disponiveis = Teste.query.filter_by(ativo=True).all()
    
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
    
    return render_template('pages/student.html', testes_info=testes_info)


@bp.route('/prova/<int:teste_id>')
def show(teste_id):
    return render_template('pages/exame.html')