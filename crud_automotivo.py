#-*- coding: utf-8 -*-
__author__ = 'infante'

from flask.ext.admin.base import BaseView, expose
from flask.helpers import make_response
from flask import Flask, render_template, send_from_directory,\
    request, redirect, url_for
from mongoengine import connect
from mongoengine.queryset import Q
from flask.ext.mongoengine import MongoEngine
from flask.ext.admin import Admin
from flask.ext import login
from wtforms import form, fields

import os

#import configuracoes do banco
from conf import DB_NAME, DB_USERNAME, DB_PASSWORD, DB_HOST_ADDRESS

#importa modelos, views de admin e forms
from admin import ViewUsuario, ViewFabricante, ViewAutomovel, MyAdminIndexView
from models import Usuario, Fabricante, Automovel
from forms import FormLogin

#inicia configuracao do app
app = Flask(__name__, static_url_path='/static')

app.config['SECRET_KEY'] = '\xfacmJ\xbd\x99\xa5\x84z\xda\xfcHD\x15O\xf4\xdff\x8d*'
app.config["MONGODB_DB"] = DB_NAME

app.config.update(
    DEBUG=False,
)

#configura login_manager
login_manager = login.LoginManager()
login_manager.init_app(app)


def realiza_busca(termos):
    u"""Função para realização de busca de termos nos campos do modelo Automovel"""

    #Implementa busca por um ou mais termos simultâneos nos campos ano, modelo e fabricante
    #de um automovel

    automoveis = None

    #para cada um dos termos
    for termo in termos:
        #obtem fabricante correspondente ao termo se existir
        fabricante = Fabricante.objects().filter(Q(nome__icontains=termo))

        #se ja houver automoveis filtrados,
        if automoveis:
            #gera resultado busca extra de automoveis cujos modelos ou anos contenham ao termo buscado
            extra = Automovel.objects().filter(Q(modelo__icontains=termo) |
                                               Q(ano__icontains=termo)).order_by('fabricante.nome')
            #se busca extra gerou resultados
            if extra:
                #atualiza lista de resultadoss
                automoveis._result_cache.extend(extra._result_cache)

        #caso nao haja automoveis filtrados
        else:
            #filtra automoveis cujos modelos ou anos contenham ao termo buscado
            automoveis = Automovel.objects().filter(Q(modelo__icontains=termo) |
                                                    Q(ano__icontains=termo)).order_by('fabricante.nome')

        #caso tenha sido encontrado algum fabricante correspondente ao termo
        if fabricante:
            #e caso haja automoveis nos resultados
            if automoveis:
                #filtra resultados de acordo com o fabricante
                automoveis = automoveis.filter(Q(fabricante__in=fabricante))
            else:
                #caso nao haja, obtem resultados filtrando apenas o fabricante
                automoveis = Automovel.objects().filter(Q(fabricante__in=fabricante))

    #retorna resultados
    return automoveis


def aplica_filtros(f_ano, f_fabricante, f_modelo, automoveis):
    u"""Função que aplica filtros de ano, fabricante e modelo em automoveis"""

    #filtra fabricantes contidos na lista de fabricantes
    fabricantes = Fabricante.objects().filter(nome__in=f_fabricante)
    #filtra automoveis
    autos = automoveis.filter(Q(ano__in=f_ano) |
                              Q(fabricante__in=fabricantes) |
                              Q(modelo__in=f_modelo))
    return autos

#Cria funcao de user_loader
@login_manager.user_loader
def load_user(user_id):
    return Usuario.objects(id=user_id).first()


#configura conexao ao banco
connect(DB_NAME, host='mongodb://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST_ADDRESS)
db = MongoEngine(app)

#configura rota para retornar template personalizado para erro 404
@app.errorhandler(404)
def page_not_found(error):
    u"""Funcao para servir pagina de erro 404"""
    return render_template('404.html'), 404

#configura rota para retornar template personalizado para erro 403
@app.errorhandler(403)
def page_forbidden(error):
    u"""Funcao para servir pagina de erro 403"""
    return render_template('403.html'), 403

#configura rota para retornar template personalizado para erro 410
@app.errorhandler(410)
def page_gone(error):
    u"""Funcao para servir pagina de erro 410"""
    return render_template('410.html'), 410

#configura rota para retornar template personalizado para erro 500
@app.errorhandler(500)
def internal_error(error):
    u"""Funcao para servir pagina de erro 500"""
    return render_template('500.html'), 500

#configura rota para servir favicon
@app.route('/favicon.ico')
def favicon():
    u"""Funcao para servir arquivo favicion"""
    return send_from_directory(os.path.join(app.root_path, 'static/img/'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

#configura rota para pagina inicial da aplicacao
@app.route('/', methods=('GET', 'POST'))
def index():
    u"""Funcao para tratamento da apresentacao da pagina incial"""

    #intancia formulario de filtros
    form_filtro = FormFiltros()
    #coleta todos os automoveis cadastrados
    automoveis = Automovel.objects.all().order_by('fabricante.nome')

    #cas seja um post
    if request.method == 'POST':
        #obtem os termos buscados e verifica se nao sao vazios, nesse caso,
        #chama funcao para realizar busca
        termos = request.form.get('busca')
        if termos.split(" ")[0] != "":
            automoveis = realiza_busca(termos.lower().split(" "))

        #obtem os valores dos tres possiveis filtros
        anos = request.form.get('filtro_ano')
        fabricantes = request.form.get('filtro_fabricante')
        modelos = request.form.get('filtro_modelo')

        #se pelo menos um deles nao for vazio
        if anos or fabricantes or modelos:
            #chama funcao para aplicacao dos filtros nos automoveis
            automoveis = aplica_filtros(anos.split(","),
                                        fabricantes.split(","),
                                        modelos.split(","),
                                        automoveis)

        #retorna pagina com os valores adequados
        return render_template('index.html',
                               user=login.current_user,
                               automoveis=automoveis,
                               busca=termos,
                               filtros=form_filtro,
                               anos=anos,
                               fabricantes=fabricantes,
                               modelos=modelos)

    else:
        return render_template('index.html',
                               user=login.current_user,
                               automoveis=automoveis,
                               busca="",
                               filtros=form_filtro,
                               anos="",
                               fabricantes="",
                               modelos="")


#configura rota para servir imagens
@app.route('/images/<pid>', methods=['GET'])
def serve_imagem(pid):
    u"""Funcao para servir imagens de veiculos cadastrados"""

    #obtem automovel pelo id, le os dados de sua imagem e os retorna na resposta
    automovel = Automovel.objects(pk=pid).first()
    b_image = automovel.foto.read()
    response = make_response(b_image)
    response.headers['Content-Type'] = automovel.foto.contentType
    return response

#configura rota para pagina de login
@app.route('/login/', methods=('GET', 'POST'))
def view_login():
    u"""Funcao para servir e tratar pagina e funcionalidade de login"""

    #form instancia form de login com os dados da requisicao
    form = FormLogin(request.form)
    if request.method == 'POST':
        #caso seja um post, se login valido, loga usuario e o retorna para pagina inicial
        if form.validate_login():
            user = form.obtem_usuario()
            login.login_user(user)
            return redirect(url_for('index'))
        else:
            #caso contrario retorna pagina de login mostrando os erros de validacao
            return render_template('form.html', user=login.current_user, form=form)
    else:
        #caso nao seja um post, mostra formulario vazio para usuario realizar login
        form = FormLogin()
        return render_template('form.html', user=login.current_user, form=form)

#configura rota para pagina/funcionalidade de logout
@app.route('/logout/')
def view_logout():
    u"""Funcao para tratar logout de usuario"""

    #realiza logout de usuario e o redireciona para pagina inicial
    login.logout_user()
    return redirect(url_for('index'))


#configura view para utilizacao na interface de admin e sua rota
class Raiz(BaseView):
    u"""View da interface de admin para retornar para pagina inicial"""

    @expose('/')
    def index(self):
        u"""Funcao para redirecionar usuario para pagina inicial"""
        return redirect(url_for('index'))


#formulario para filtros
class FormFiltros(form.Form):
    u"""Formulario de filtros para utilizacao na pagina inicial"""

    #obtem e ordena as opcoes para os filtros de ano, fabricante e modelo
    ano = [(opt, opt) for opt in sorted(Automovel.objects().distinct('ano'))]
    fabricante = [(opt, opt) for opt in sorted(Fabricante.objects().distinct('nome'))]
    modelo = [(opt, opt) for opt in sorted(Automovel.objects().distinct('modelo'))]

    #configura campos do formulario com as opcoes
    ano = fields.SelectMultipleField(choices=ano)
    fabricante = fields.SelectMultipleField(choices=fabricante)
    modelo = fields.SelectMultipleField(choices=modelo)


#configura interface de admin e suas views
admin = Admin(app, name='Revenda Automotiva - CRUD', index_view=MyAdminIndexView())
admin.add_view(ViewUsuario(Usuario))
admin.add_view(ViewFabricante(Fabricante))
admin.add_view(ViewAutomovel(Automovel))
admin.add_view(Raiz(name=u'Página inicial', endpoint='index'))

#funcao para execucao em desenvolvimento
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8090))
    app.run(host='0.0.0.0', port=port)
