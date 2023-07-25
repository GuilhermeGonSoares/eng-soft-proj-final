from app import db
from enum import Enum
from datetime import datetime, timedelta
from .user import User
import pytz

class StatusTeste(Enum):
    PENDENTE = "pendente"
    ABERTO = "aberto"
    FECHADO = "fechado"


class Teste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    professor_matricula = db.Column(db.String(9), db.ForeignKey('user.matricula'), nullable=False)
    nota = db.Column(db.Integer, nullable=True)
    duracao = db.Column(db.Integer, nullable=False)  # em minutos
    questoes = db.relationship('Questao', backref='teste', lazy=True, cascade="all, delete-orphan")
    status = db.Column(db.Enum(StatusTeste), default=StatusTeste.PENDENTE, nullable=False)
    abertura = db.Column(db.DateTime, nullable=False)
    fechamento = db.Column(db.DateTime, nullable=False)
    caderno_respostas = db.relationship('CadernoRespostas', backref='testes', lazy=True)
    descricao = db.Column(db.Text, nullable=False)

def fechar_testes():
    saopaulo_tz = pytz.timezone('America/Sao_Paulo')
    from app import app

    with app.app_context():
        utc_now = datetime.utcnow()
        saopaulo = utc_now.replace(tzinfo=pytz.utc).astimezone(saopaulo_tz).replace(tzinfo=None)
        testes = Teste.query.filter_by(status=StatusTeste.ABERTO).all()
        for teste in testes:
            if saopaulo >= teste.fechamento:
                teste.status = StatusTeste.FECHADO
                db.session.commit()

def abrir_testes():
    saopaulo_tz = pytz.timezone('America/Sao_Paulo')
    from app import app

    with app.app_context():
        utc_now = datetime.utcnow()
        saopaulo = utc_now.replace(tzinfo=pytz.utc).astimezone(saopaulo_tz).replace(tzinfo=None)
        testes = Teste.query.filter_by(status=StatusTeste.PENDENTE).all()
        for teste in testes:
           if saopaulo >= teste.abertura:
                teste.status = StatusTeste.ABERTO
                db.session.commit()


class TipoQuestao(Enum):
    MULTIPLA_ESCOLHA = 'multipla_escolha'
    VERDADEIRO_FALSO = 'verdadeiro_falso'
    DISCURSIVA = 'discursiva'


class Questao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    teste_id = db.Column(db.Integer, db.ForeignKey('teste.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'multipla_escolha', 'verdadeiro_falso', 'discursiva'
    pontuacao = db.Column(db.Integer, nullable=False)
    texto = db.Column(db.Text, nullable=False)
    gabarito = db.Column(db.String(255), nullable=True)
    opcoes = db.relationship('Opcao', backref='questao', lazy=True, cascade="all, delete-orphan")

class Opcao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    questao_id = db.Column(db.Integer, db.ForeignKey('questao.id'), nullable=False)
    texto = db.Column(db.Text, nullable=False)
    eh_correta = db.Column(db.Boolean, nullable=False)


class CadernoRespostas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_matricula = db.Column(db.String(9), db.ForeignKey('user.matricula'), nullable=False)
    teste_id = db.Column(db.Integer, db.ForeignKey('teste.id'), nullable=False)
    finalizado = db.Column(db.Boolean, nullable=False, default=False)
    nota = db.Column(db.Integer, nullable=False, default=0)

    respostas = db.relationship('Resposta', backref='caderno_respostas', lazy=True)
    aluno = db.relationship(User, backref='caderno_respostas', lazy=True)

class Resposta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caderno_respostas_id = db.Column(db.Integer, db.ForeignKey('caderno_respostas.id'), nullable=False)
    questao_id = db.Column(db.Integer, db.ForeignKey('questao.id'), nullable=False)
    resposta = db.Column(db.Text, nullable=False)
    acertou = db.Column(db.Boolean, nullable=False, default=True)
    questao = db.relationship('Questao', backref='respostas', lazy=True)

