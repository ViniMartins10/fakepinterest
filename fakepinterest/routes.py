#rotas
from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt  #bcrypt vai criptografar a senha para segurança
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto # na tela principal terá o formulário de login e na tela de criar conta o formulario de criar conta 
from fakepinterest.models import Usuario, Foto  # Impotando as informações dos Usuarios
import os
from werkzeug.utils import secure_filename # essa biblioteca já faz o processo de transformar o nome em um nome seguro

@app.route("/", methods=["GET","POST"])#tem que permitir o metodo GET e o POST sempre que tiver um formulario e o mesmo tiver o metodo POST
def homepage():
    form_login = FormLogin()
    if form_login.validate_on_submit(): # preencheu os campo de login de forma valida
        usuario = Usuario.query.filter_by(email=form_login.email.data).first() #vai ter que procurar o usuario da mesma forma que foi feito no forms def validate_email()
        if usuario and  bcrypt.check_password_hash(usuario.senha.encode("utf-8"), form_login.senha.data) :    #se achou o usuário e # vai verificar se a senha bate, a criptografada e a senha passada no formulario     
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("homepage.html", form=form_login)#passando o formulario para o html


@app.route("/criarconta", methods=["GET","POST"])#Tela para criar conta
def criarconta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit(): #ele verifica se o usuario já clicou no botão e se todos os campos estão preenchidos e as validações foram aplicadas
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data).decode("utf-8")#criptografa a senha do usuário
        # bcrypt.check_password_hash(senha) // vê se a senha
        usuario=Usuario(username=form_criarconta.username.data, #Usuario vem da classe Usuario da Models
                        senha= senha,
                        email=form_criarconta.email.data) # pega as informações
        database.session.add(usuario) # adiciona na sessão do banco de dados
        database.session.commit() # esse executa tudo que você quer fazer no add
        login_user(usuario, remember=True) #tem que estar logado para entrar na aba de perfil
        return redirect(url_for("perfil", id_usuario=usuario.id))#passa como paramÊtro o username do usuario para redirecionar  
    return render_template("criarconta.html", form=form_criarconta)#passando o formulario para o html



@app.route("/perfil/<id_usuario>", methods = ["GET","POST"])# informação unica
@login_required # atributo de segurança que só pode ser acessada quando o usuário estiver logado
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id): #se oo usuario ta vendo o perfil dele mesmo
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data #PEGA O ARQUIVO 
            nome_seguro = secure_filename(arquivo.filename) # para não ter erro de caracters especiais no código iremos corrigir o nome
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),# esse nome significa o projeto e o __file__ significa esse arquivo
                              app.config["UPLOAD_FOLDER"], nome_seguro) #o caminho vai ser o próprio caminho do projeto, o app.config[UPLOAD_FOLDER], nome seguro o app.config está no init
            arquivo.save(caminho) #salvar o arquivo na pasta fotos_post
            foto = Foto(imagem= nome_seguro, id_usuario=current_user.id) #registrar esse arquivo no banco de dados/importando a classe Foto da Models
            database.session.add(foto)
            database.session.commit()#processo para adicionar a foto no banco de dados, no caso o nome .png
        return render_template("perfil.html", usuario=current_user, form = form_foto)#esse formulario será carregado no perfil html
    else:
        usuario = Usuario.query.get(int(id_usuario))  #pra encontrar um id de um usuário basta usar um get, na model tem um exemplo, @login_manager.user_loader
        return render_template("perfil.html", usuario = usuario, form = None)#pegar informação e enviar para o html nesse formato


@app.route("/logout")
@login_required
def logout():
    logout_user() # função para deslogar o usuario atual, não precisa do current user o logout já sabe que é o atual
    return redirect(url_for('homepage'))


@app.route("/feed")
@login_required  # só vai poder entrar no feed quem estiver logado
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
    return render_template("feed.html", fotos = fotos) #quando a pessoa entrar no feed vai entrar nessa tela ("feed.html")