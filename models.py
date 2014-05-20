#-*- coding: utf-8 -*-
__author__ = 'infante'

from mongoengine import *
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(Document):
    u"""Modelo para usuário da aplicação"""

    #opcoes para escolha de permissao do usuario
    opcoes = (('admin', u'Administrador'),
              ('editor', u'Editor'),)

    #campo de email, campo unico para cada usuario
    email = EmailField(verbose_name=u"E-mail",
                       required=True,
                       unique=True,
                       help_text=u"Informe um e-mail válido do novo usuário.")

    #campo de nome do usuario
    nome = StringField(verbose_name=u"Nome",
                       max_length=50,
                       required=True,
                       help_text=u"Informe o nome do usuário.")

    #campo de sobrenome do usuario
    sobrenome = StringField(verbose_name=u"Sobrenome",
                            max_length=50,
                            help_text=u"Informe o sobrenome do usuário.")

    #campo de senha do usuario
    chave = StringField(verbose_name=u"Senha",
                        max_length=50,
                        required=True,
                        help_text=u"Informe a senha do novo usuário.")

    #campo de permissao do usuario
    permissao = StringField(verbose_name=u"Permissão",
                            max_length=25,
                            required=True,
                            choices=opcoes,
                            help_text=u"Informe nível de permissão do usuário.")

    #campo que indica se usuario está ativo
    ativo = BooleanField(verbose_name=u"Ativo",
                         help_text=u"Informe se usuário está ativo.",
                         default=True)

    def __init__(self, chave=None, **data):
        u"""Método personalizado de inicialização de instância do modelo"""

        #durante inicializacao da instância, 'criptografa' senha do usuario
        if chave is not None:
            data['chave'] = generate_password_hash(chave)
        super(Usuario, self).__init__(**data)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def checa_chave(self, chave):
        return check_password_hash(self.chave, chave)

    def __unicode__(self):
        u"""Método que retorna representação unicode do objeto"""
        return self.email


class Fabricante(Document):
    u"""Modelo para registro de fabricantes de automóveis utilizados na aplicação"""

    #campo de nome do fabricante
    nome = StringField(verbose_name=u"Nome",
                       max_length=30,
                       required=True,
                       help_text=u"Informe o nome do fabricante.")

    def __unicode__(self):
        u"""Método que retorna representação unicode do objeto"""
        return self.nome


class Automovel(Document):

    u"""Modelo para registros de automóveis utilizados pela aplicação"""
    ano = StringField(verbose_name=u"Ano",
                      help_text=u"Informe o ano de fabricação deste automóvel.",
                      required=True,
                      max_length=4,
                      min_length=4)
    fabricante = ReferenceField(Fabricante,
                                verbose_name=u"Fabricante",
                                required=True,
                                help_text=u"Informe o fabricante deste automóvel.")
    modelo = StringField(verbose_name=u"Modelo",
                         max_length=75,
                         required=True,
                         help_text=u"Informe o modelo deste automóvel.")
    foto = ImageField(verbose_name=u"Foto",
                      required=True,
                      help_text=u"Insira uma imagem do automóvel.",
                      size=(800, 600, True))

    def __unicode__(self):
        u"""Método que retorna representação unicode do objeto"""
        return "_".join([self.modelo, str(self.ano)])





