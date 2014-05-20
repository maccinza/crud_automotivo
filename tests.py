#-*- coding: utf-8 -*-
__author__ = 'infante'

import sys
import unittest
import flask

from flask.ext.mongoengine import MongoEngine

#TODO: implementar testes

#Alguns casos de testes

# - Aplicacao Up
# - Aplicacao Down

# - Login
#  - Parametros corretos, e-mail e senha válidos
#  - Parametros incorretos, e-mail vazio
#  - Parametros incorretos, e-mail inválido
#  - Parametros incorretos, e-mail inexistente no sistema
#  - Parametros incorretos, senha vazia
#  - Parametros incorretos, senha com menos de 8 caracteres
#  - Parametros incorretos, senha inválida para o e-mail informado

# - Criacao/Edicao/Delecao
#  - Acesso aos modelos de administracao com usuario sem permissoes
#  - Acesso aos modelos de administracao com usuario com permissoes
#  - Fabricantes
#   - Criacao/Edicao com nome vazio,
#   - Criacao/Edicao com nome válido
#   - Delecao de fabricante nao referenciado por um automovel
#   - Delecao de fabricante referenciado por um automovel
#  - Automoveis
#   - Criacao/Edicao com ano incorreto com valor não numérico (atualmente falha)
#   - Criacao/Edicao com ano incorreto com valor menor ou maior que 4 digitos
#   - Criacao/Edicao com fabricante vazio,
#   - Criacao/Edicao com modelo vazio,
#   - Criacao/Edicao sem foto (Problema conhecido,
#     edição pede sempre uma foto mesmo que já exista: https://github.com/mrjoes/flask-admin/pull/370)
#   - Criacao/Edicao com foto muito grande (TODO: implementar validator para tamanho maximo)
#   - Delecao de automovel
#  - Usuarios
#   - Criacao/Edicao com e-mail vazio
#   - Criacao/Edicao com e-mail inválido
#   - Criacao/Edicao com nome vazio
#   - Criacao/Edicao com senha vazia
#   - Criacao/Edicao com senha de comprimento menor que 8 caracteres
#   - Criacao/Edicao com confirmacao de senha vazia
#   - Criacao/Edicao com senha e confirmacao diferentes
#   - Criacao/Edicao com valores validos, usuario administrador ativo/inativo
#   - Criacao/Edicao com valores validos, usuario editor ativo/inativo

# - Acessar página de login através da página inicial
# - Após estar logado, acessar página de administração através da página inicial
# - Realizar busca vazia
# - Realizar busca com um e com mais de um termo simultaneamente
# - Realizar filtragens combinadas
# - Realizar busca com filtragem
# - Visualizar página de resultado de busca/filtro sem resultados
# - Remover filtros
# - Realizar Logout
