#criar formularios do site
from collections.abc import Sequence
from typing import Any, Mapping
from flask_wtf import FlaskForm  #estrutura dos formularios
from wtforms import StringField, PasswordField, SubmitField, FileField #os campos de texto, número data..., Filefield é de arquivo
from wtforms.validators import DataRequired, Email,EqualTo, Length, ValidationError    #DataRequired = usuario terá que preencher o campo,EqualTo para ver se um campo é igual a outro, ValidationError para quando der erro aparecer uma mensagem.
from fakepinterest.models import Usuario

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()]) #nome do campo que o usuário vai ver
    senha = PasswordField("Senha",validators=[DataRequired()])#
    botao_confirmacao = SubmitField("Fazer Login", )#

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first() # verificar no banco, vem do Model essa informação, campo email primerio é o campo do usuario
        if not usuario: # se já existe um usuário, se a lista tem alguma informação
            raise ValidationError("Usuário inexistente. crie uma conta para continuar")


class FormCriarConta(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("Nome de usuário", validators=[DataRequired()])
    senha = PasswordField("Senha", validators= [DataRequired(),Length(6,20)])
    confirmacao_senha = PasswordField("Senha",[DataRequired(), EqualTo("senha")])#Passa o nome do campo que deve ser igual
    botao_confirmacao = SubmitField("Criar Conta")



    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first() # verificar no banco, vem do Model essa informação, campo email primerio é o campo do usuario
        if usuario: # se já existe um usuário, se a lista tem alguma informação
            raise ValidationError("E-mail já cadastrado, faça login para continuar")
        

class FormFoto(FlaskForm):
    foto = FileField("Foto", validators=[DataRequired()]) #
    botao_confirmacao = SubmitField("Enviar")