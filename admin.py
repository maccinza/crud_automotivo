#-*- coding: utf-8 -*-
__author__ = 'infante'

from flask.ext.admin.contrib.mongoengine import ModelView
from flask.ext.admin import AdminIndexView
from flask.ext import login

from models import Usuario, Automovel, Fabricante
from forms import FormCriacaoUsuario


class MyAdminIndexView(AdminIndexView):
    u"""Definição de view de entrada de administração"""

    def is_accessible(self):
        u"""Método que indica se view está acessível"""

        #view está acessível se usuário estiver autenticado
        return login.current_user.is_authenticated()


class ViewUsuario(ModelView):
    u"""Definição de view de administração para Usuário"""

    #indica que deve utilizar form personalizado
    form = FormCriacaoUsuario

    #configura campos que poderao ser filtrados, que serao exibidos na listagem e que serao buscaveis
    column_filters = ['nome']
    column_list = ['nome', 'sobrenome', 'email', 'permissao', 'ativo']
    column_searchable_list = ('nome', 'sobrenome', 'email')

    def is_accessible(self):
        u"""Método que indica se view está acessível"""

        # se usuário estiver autenticado, possuir permissao de administrador e estiver ativo
        if login.current_user.is_authenticated():
            user = Usuario.objects(email=login.current_user.email).first()
            if user.permissao == "admin" and user.ativo:
                #libera acesso à view
                return True
        #bloqueia acesso à view caso contrario
        return False

    def is_visible(self):
        u"""Método que indica se view está visível"""

        #retorna mesma resposta do método que indica se está acessivel
        return self.is_accessible()


class ViewFabricante(ModelView):
    u"""Definição de view de administração para Fabricante"""

    #configura campos que poderao ser filtrados e que serao buscaveis
    column_filters = ['nome']
    column_searchable_list = ('nome', )

    def is_accessible(self):
        u"""Método que indica se view está acessível"""

        #libera acesso se usuario esta autenticado e ativo
        return login.current_user.is_authenticated() and login.current_user.ativo

    def delete_model(self, model):
        u"""Método personalizado para tratamento de deleção"""

        #verifica se fabricante está sendo usado em algum automovel
        fabricante = Fabricante.objects().filter(nome=model.nome).first()
        autos = Automovel.objects().filter(fabricante=fabricante)
        if not autos:
            #caso nao esteja, executa delecao
            super(ViewFabricante, self).delete_model(model)
            return True
        return False


class ViewAutomovel(ModelView):
    u"""Definição de view de administração para Automovel"""

    #configura campos que poderao ser filtrados e que serao buscaveis
    column_filters = ['ano']
    column_searchable_list = ('modelo',)

    def is_accessible(self):
        u"""Método que indica se view está acessível"""

        #libera acesso se usuario esta autenticado e ativo
        return login.current_user.is_authenticated() and login.current_user.ativo