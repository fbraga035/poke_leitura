import pandas as pd
from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)


@app.route('/')
def homepage():
  resposta = {'total_vendas': 'total_vendas'}
  return jsonify(resposta)
 

def select_pode_ir():
  # Conexão e cursor
  conexao = sqlite3.connect("poke.db")
  cursor = conexao.cursor()

  sql = "SELECT pode_ir_f, pode_ir_b FROM pode_ir;"

  cursor.execute(sql)

  # Extraindo os valores das colunas
  for row in cursor.fetchall():
    pode_ir_f = row[0]
    pode_ir_b = row[1]

  conexao.close()
  return pode_ir_f, pode_ir_b


def pegar_vendas():
  pode_ir_f, pode_ir_b = select_pode_ir()
  resposta = {'total_vendas': pode_ir_b}
  return jsonify(resposta)


def atualizar_vendas():
  novas_vendas = request.get_json()['total_vendas']

  conexao = sqlite3.connect("poke.db")
  cursor = conexao.cursor()

  sql = "UPDATE pode_ir SET pode_ir_b = ?"
  cursor.execute(sql, (novas_vendas, ))

  conexao.commit()
  conexao.close()

  return jsonify({'mensagem': 'Vendas atualizadas com sucesso!'})


@app.route('/pegarvendas', methods=['GET'])
def pegar_vendas_rota():
  return pegar_vendas()


@app.route('/atualizarvendas', methods=['PUT'])
def atualizar_vendas_rota():
  return atualizar_vendas()


app.run(host='0.0.0.0')
