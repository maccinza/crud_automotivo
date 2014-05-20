#-*- coding: utf-8 -*-
__author__ = 'infante'

from wtforms import form, fields, validators
from flask.ext.mongoengine.wtf.orm import model_form
from models import Usuario, Automovel, Fabricante


class FormCriacaoUsuario(model_form(Usuario)):
    u"""Formuário personalizado para criação de Usuario na interface de admin"""

    #configura campo de senha e seus validadores
    chave = fields.PasswordField(
        u'Senha',
        [validators.required(),
         validators.Length(min=8),
         validators.equal_to('confirmacao', message='Senhas precisam coincidir.')])

    #configura campo de confirmação de senha
    confirmacao = fields.PasswordField(u'Confirmação de Senha')


class FormCriacaoAutomovel(model_form(Automovel)):
    u"""Formuário personalizado para criação de Automovel na interface de admin"""

    #Obsoleto
    #TODO: Estudar como utilizar form customizado para validar ano de fabricação
    #TODO: e

    #configura campo ano e seus validadores
    ano = fields.TextField(
        u'Ano',
        [validators.required(),
         validators.Length(min=4, max=4)])

    #configura campo foto e seus validadores
    foto = fields.FileField(u'Foto',
                            [validators.regexp(u'.\.jpg$')])


class FormLogin(form.Form):
    u"""Formulário personalizado para login de Usuario"""

    #configura campo de e-mail e seus validadores
    email = fields.TextField(u'E-mail:',
                             validators=[validators.required(),
                                         validators.email()])

    #configura campo de senha e seus validadores
    chave = fields.PasswordField(u'Senha:',
                                 validators=[validators.required(),
                                             validators.Length(min=8)])

    def validate_login(self):
        u"""Método para validar login do Usuario"""

        #valida campos do formulario e retorna falso caso nao valide
        rv = form.Form.validate(self)
        if not rv:
            return False

        #obtem usuario com o email do login
        usuario = self.obtem_usuario()

        #caso nao consiga obter usuario, retorna erro de que e-mail nao está registrado
        if usuario is None:
            self.email.errors.append(u'E-mail not registered.')
            return False

        #verifica se a senha informada confere para o usuario
        if not usuario.checa_chave(self.chave.data):
            self.chave.errors.append(u'Incorrect password.')
            return False
        return True

    def obtem_usuario(self):
        u"""Método que obtem usuário a partir do valor indicado no campo email do formulario"""
        return Usuario.objects(email=self.email.data).first()
