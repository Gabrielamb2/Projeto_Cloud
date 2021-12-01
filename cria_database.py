import boto3
from botocore.config import Config
from cria_instancia import create_instance
from read import read_command

# Referências: 
#     https://stackoverflow.com/questions/3777301/how-to-call-a-shell-script-from-python-code/3777351

def create_database(regiao,imagem,tipo_instancia,nome,grupo_segurnaca,key_name):
    #ler o arquivo
    print("Criando Database {0}".format(nome))
    user_data = '''#!/bin/bash
        cd /
        sudo apt update
        sudo apt install postgresql postgresql-contrib -y
        sudo -u postgres createuser cloud
        sudo -u postgres createdb tasks -O cloud
        sudo sed -i s/"^#listen_addresses = 'localhost'"/"listen_addresses = '*'"/g  /etc/postgresql/10/main/postgresql.conf
        sudo sed -i '$a host all all 0.0.0.0/0 trust' /etc/postgresql/10/main/pg_hba.conf
        sudo ufw allow 5432/tcp
        sudo systemctl restart postgresql
        '''
    instancia,instancia_public_ip_address, instancia_instance_id = create_instance(regiao,imagem,tipo_instancia,nome,grupo_segurnaca,key_name,UserData=user_data)
    print("Database {0} criado".format(nome))
    return instancia,instancia_public_ip_address, instancia_instance_id