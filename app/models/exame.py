from app import db
from enum import Enum
from datetime import datetime, timedelta

class Teste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professor_matricula = db.Column(db.String(9), db.ForeignKey('user.matricula'), nullable=False)
    duracao = db.Column(db.Integer, nullable=False)  # em minutos
    questoes = db.relationship('Questao', backref='teste', lazy=True)
    ativo = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    caderno_respostas = db.relationship('CadernoRespostas', backref='testes', lazy=True)

def fechar_testes():
    from app import app

    with app.app_context():
        testes = Teste.query.filter_by(ativo=True).all()
        for teste in testes:
            if (datetime.utcnow() - teste.created_at) > timedelta(minutes=teste.duracao):
                teste.ativo = False
                db.session.commit()

class TipoQuestao(Enum):
    MULTIPLA_ESCOLHA = 'multipla_escolha'
    VERDADEIRO_FALSO = 'verdadeiro_falso'
    DISCURSIVA = 'discursiva'


class Questao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teste_id = db.Column(db.Integer, db.ForeignKey('teste.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'multipla_escolha', 'verdadeiro_falso', 'discursiva'
    pontuacao = db.Column(db.Integer, nullable=False)
    texto = db.Column(db.Text, nullable=False)
    gabarito = db.Column(db.String(255), nullable=False)
    opcoes = db.relationship('Opcao', backref='questao', lazy=True)

class CadernoRespostas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_matricula = db.Column(db.String(9), db.ForeignKey('user.matricula'), nullable=False)
    teste_id = db.Column(db.Integer, db.ForeignKey('teste.id'), nullable=False)
    finalizado = db.Column(db.Boolean, nullable=False, default=False)
    nota = db.Column(db.Integer, nullable=False, default=0)

    respostas = db.relationship('Resposta', backref='caderno_respostas', lazy=True)

class Resposta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caderno_respostas_id = db.Column(db.Integer, db.ForeignKey('caderno_respostas.id'), nullable=False)
    questao_id = db.Column(db.Integer, db.ForeignKey('questao.id'), nullable=False)
    resposta = db.Column(db.Text, nullable=False)
    acertou = db.Column(db.Boolean, nullable=False, default=True)
    questao = db.relationship('Questao', backref='respostas', lazy=True)

class Opcao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    questao_id = db.Column(db.Integer, db.ForeignKey('questao.id'), nullable=False)
    texto = db.Column(db.Text, nullable=False)
    letra = db.Column(db.String(1), nullable=False)
    eh_correta = db.Column(db.Boolean, nullable=False)
