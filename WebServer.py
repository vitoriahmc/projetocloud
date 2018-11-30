from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/Tarefa", methods=['POST'])
def tarefas():

	if request.method == 'POST':

		try:

			q = int(request.get_json())
			q = str(q**2)

			return q

		except:

		 	print("POST /Tarefa not ok")

	else:

		print("Erro")

@app.route("/healthcheck/")
def healthcheck():
	print("Health check ok")
	return "200"
