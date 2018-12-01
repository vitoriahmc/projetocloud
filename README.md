O meu projeto cria um loadbalancer que é responsável por criar 3 máquinas. 

Ao criar, ele guarda seus IPs em uma lista e confere se as instâncias ainda estão rodando ou não. 

Caso a instância não esteja mais rodando, ele criará novas para dividir as requisições.

A requisição escolhida foi realizar uma operação matemática. Dessa maneira, o client insere como input um número e esse número será elevado ao quadrado no WebServer.



Para rodar o programa, o usuário deve criar uma instância na AWS, entrar nela via SSH e rodar as seguinte linhas de comando:


sudo apt -y update
sudo apt install -y python-pip 
sudo apt install snapd
pip install boto3
pip install awscli --upgrade --user
pip install Flask
pip install requests
sudo apt install snapd
sudo snap install aws-cli --classic


git clone https://github.com/vitoriahmc/projetocloud.git
cd projetocloud


Depois você deve entrar com suas credenciais na AWS com a seguinte linha de comando:

aws configure

Por fim, rode: 

export FLASK_APP=init.py
python -m flask run --host=0.0.0.0


