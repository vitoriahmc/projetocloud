#!/usr/bin/env
# -*- coding: utf-8 -*-

#Fonte: https://gist.github.com/ableasdale/8cb7a61cad3202e09bab3e11c4639133

import boto3
import sys
from flask import Flask, request
import json
import requests
from random import randint
import threading

resources = boto3.resource('ec2',region_name='us-east-1')
client = boto3.client('ec2',region_name='us-east-1')

try: 
	response = client.delete_key_pair(
	KeyName = 'vitoria',
	DryRun = False
	)

except:
	print("Não achou key")

try:

	file = open('vitoria.pub','r')

	response = client.import_key_pair(
	KeyName = 'vitoria',
	DryRun = False,
	PublicKeyMaterial=file.read()
	)
	file.close()

except:

	print ("Não criou key")

	response = client.describe_key_pairs(
			    
	KeyNames=[
		'vitoria',
			],
	DryRun=False
	)

try:

	response = client.delete_security_group(
	    GroupName='APS-vi',
	    GroupId='sg-0354a023290c37aa1',
	    DryRun=False
	)

except:
	print("Não apagou security group")

try:

	response = client.create_security_group(
    Description='proj-cloud',
    GroupName='APS-vi',
    DryRun=False
	)

	client.authorize_security_group_ingress(
	GroupId=response['GroupId'],
	IpProtocol="tcp",
	CidrIp="0.0.0.0/0",
	FromPort=22,
	ToPort=22
	)

	client.authorize_security_group_ingress(
	GroupId=response['GroupId'],
	IpProtocol="tcp",
	CidrIp="0.0.0.0/0",
	FromPort=5000,
	ToPort=5000
	)
	client.authorize_security_group_ingress(
	GroupId=response['GroupId'],
	IpProtocol="tcp",
	CidrIp="0.0.0.0/0",
	FromPort=80,
	ToPort=80
	)

except:

	print("Não criou security group")

ip_instancias = []
def criaInstancia(user_data, n, ip_lista):
	
	for i in range(n):
		try:

			instance = resources.create_instances(

			    ImageId='ami-0ac019f4fcb7cb7e6',
			    MinCount=1,
			    MaxCount=1,
			    KeyName='vitoria',
			    InstanceType='t2.micro',
			    UserData=user_data,
			    TagSpecifications=[
		        {
		            'ResourceType': 'instance',
		            'Tags': [
		                {
		                    'Key': 'Owner',
		                    'Value': "Vitoria"
		                },
		            ]
		        },
		    ],
			    SecurityGroupIds=[response['GroupId']])

			print("Waiting...")

			instance = instance[0]

			instance.wait_until_running()

			instance.load()

			ip_lista.append(instance.public_ip_address)

		except:

			print("Não criou a instancia")
 
userdata = """#!/bin/bash
	cd home
	cd ubuntu
	sudo apt -y update
	sudo apt install snapd
	sudo apt install -y python-pip 
	git clone https://github.com/vitoriahmc/projetocloud.git
	pip install boto3
	pip install Flask
	pip install requests
	cd projetocloud
	export FLASK_APP=lb.py
	python -m flask run"""

userdata2 = """#!/bin/bash
	cd home
	cd ubuntu
	sudo apt -y update
	sudo apt install snapd
	sudo apt install -y python-pip 
	git clone https://github.com/vitoriahmc/projetocloud.git
	pip install boto3
	pip install Flask
	pip install requests
	cd projetocloud
	export FLASK_APP=WebServer.py
	python -m flask run"""


criaInstancia(userdata, 1, ip_instancias)

print("IP do LoadBalancer: ", ip_instancias[0])

def healthcheck(ip_lista):

	while(True):

		for instance in resources.instances.all():

			if instance.public_ip_address in ip_instancias and instance.state['Name'] != 'running':

				ip_instancias.remove(instance.public_ip_address)

		while len(ip_instancias) < 4:

			criaInstancia(userdata2,1,ip_instancias)

		num = randint(1,len(ip_instancias)-1)
		random_ip = ip_instancias[num]

		endereco = "http://{0}:5000/Tarefa".format(str(random_ip))

threading.Thread(target=healthcheck, args = [ip_instancias]).start()

app = Flask(__name__)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):

	if request.method == 'POST':

		try:

			valor = request.get_json()
			res = requests.post(endereco, json=valor)
			print(res)

			return res.text

		except:

		 	print("Erro no POST")

	else:

		print("Erro")

if __name__ == '__main__':

	app.run(host='0.0.0.0')