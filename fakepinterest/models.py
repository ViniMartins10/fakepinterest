#estrutura do banco de dados
from fakepinterest import database, login_manager #fakepinterest aponta para a __init__ e suas funções
from datetime import datetime
from flask_login import UserMixin # diz qual é a classe que vai gerenciar a estrutura de logins

@login_manager.user_loader #aqui você diz que é a função que carrega o usuário é a de baixo
def load_usuario(id_usuario): #recebe um id e retorna quem é o usuario(função obrigatória)
    return Usuario.query.get(int(id_usuario)) # retorna um usuario específico

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable = False)
    email = database.Column(database.String, nullable = False, unique=True)
    senha = database.Column(database.String, nullable=False)
    fotos = database.relationship("Foto", backref="usuario", lazy= True)

#relatioship é para relacionar tabelas, nesse caso a tabela usuario com fotos, o backref é o caminho oposto, usuario -> fotos, fotos -> usuario


class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default="default.png")
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    id_usuario =  database.Column(database.Integer, database. ForeignKey('usuario.id'), nullable=False)
