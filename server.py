# coding: utf-8
import json
from flask import Flask
from flask import request, send_from_directory, render_template

import sports as sp

app = Flask(__name__)
@app.route('/')
def server():
    return render_template("index.html")
@app.route('/api', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api():
  if request.method == 'GET':
    return json.dumps({'descricao': 'API RESTful de exemplo', 'versao': '0.1'})
  else:
    return json.dumps({'erro': 'Método inválido'})

@app.route('/js/<path:path>')
def send_js(path):
  return send_from_directory('js', path)

@app.route('/enviar', methods=['POST'])
def post():
  noticia = request.form.get('noticia')
  if noticia:
    noticia = sp.testa(noticia) * 100
  return render_template("index.html", noticia=noticia)
@app.route('/put', methods=['PUT'])
def put():
  return json.dumps({'mensagem': 'Requisição PUT recebida', 'dados':
  request.form['dados']})
@app.route('/delete/<recurso>', methods=['DELETE'])
def delete(recurso):
  return json.dumps({'mensagem': u'Requisição DELETE para o recurso de nome: ' + recurso})
if __name__ == "__main__":
  app.run(debug=True)
