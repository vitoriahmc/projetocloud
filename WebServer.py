from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/Tarefa", methods=['POST', 'GET'])
def tarefas():

	if request.method == 'GET':

		pass

	else:

		try:

			q = int(request.get_json())
			q = str(q**2)

			return q

		except:

		 	print("POST /Tarefa not ok")

@app.route("/healthcheck/")
def healthcheck():
	print("Health check ok")
	return "200"
