from app import db
from enum import Enum
from datetime import datetime

class Teste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professor_matricula = db.Column(db.String(9), db.ForeignKey('user.matricula'), nullable=False)
    duracao = db.Column(db.Integer, nullable=False)  # em minutos
    questoes = db.relationship('Questao', backref='teste', lazy=True)
    respostas = db.relationship('Resposta', backref='teste', lazy=True)
    ativo = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

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

class Resposta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_matricula = db.Column(db.String(9), db.ForeignKey('user.matricula'), nullable=False)
    questao_id = db.Column(db.Integer, db.ForeignKey('questao.id'), nullable=False)
    resposta = db.Column(db.Text, nullable=False)
    teste_id = db.Column(db.Integer, db.ForeignKey('teste.id'), nullable=False)

class Opcao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    questao_id = db.Column(db.Integer, db.ForeignKey('questao.id'), nullable=False)
    texto = db.Column(db.Text, nullable=False)
    eh_correta = db.Column(db.Boolean, nullable=False)
