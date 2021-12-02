import boto3
from botocore.config import Config
from cria_instancia import create_instance
from cria_database import create_database
from cria_security_group import create_security_group
from deleta_instancia import terminate_instance 
from deleta_security_group import terminate_security_groups
from ami import create_image, delete_image
import json
import time

#AWS KEYS 
KEY_NAME='testeinstancia1'

# CONFIGURAÇÃO POSTGRESQL
POSTGRESQL_NOME='Postgresql'
POSTGRESQL_REGIAO='us-east-2'
POSTGRESQL_IMAGEM='ami-020db2c14939a8efb'
POSTGRESQL_TIPO_INSTANCIA='t2.micro'
POSTGRESQL_SECURITY_GROUP='testePostgres'

# CONFIGURAÇÃO NORTH VIRGINIA
NORTH_VIRGINIA_NOME = 'North-Virigina'
NORTH_VIRGINIA_REGIAO = 'us-east-1'
NORTH_VIRGINIA_IMAGEM = 'ami-0279c3b3186e54acd'
NORTH_VIRGINIA_TIPO_INSTANCIA= 't2.micro'
NORTH_VIRGINIA_SECURITY_GROUP = 'testNorthVirginia'


# CLIENTS AND WAITERS ---------------------------------------------
ohio_client = boto3.client('ec2', region_name=POSTGRESQL_REGIAO)
ohio_waiter_terminate = ohio_client.get_waiter('instance_terminated')

north_virginia_client = boto3.client('ec2', region_name=NORTH_VIRGINIA_REGIAO)
north_virginia_waiter_terminate = north_virginia_client.get_waiter('instance_terminated')

north_virginia_waiter_ami = north_virginia_client.get_waiter('image_available')



# DELETANDO INSTÂNCIA
terminate_instance(ohio_client, ohio_waiter_terminate)
print()
terminate_instance(north_virginia_client, north_virginia_waiter_terminate)
print()

# DELETANDO AMIS
delete_image(north_virginia_client)
print()

# DELETANDO SECURITY GROUPS
terminate_security_groups(ohio_client)
print()
terminate_security_groups(north_virginia_client)
print()


# CRIANDO SECURITY GROUPS
with open('security_group.txt', 'r') as file:
        postgresql_ports_and_protocols=json.load(file)

POSTGRES_SECURITY_GROUP = create_security_group(POSTGRESQL_REGIAO,POSTGRESQL_SECURITY_GROUP,'Habilitar portas','postgres_databese',postgresql_ports_and_protocols)
print()

with open('django_security_group.txt', 'r') as file:
        north_virginia_ports_and_protocols=json.load(file)

NORTH_VIRGINIA_SECURITYs_GROUP = create_security_group(NORTH_VIRGINIA_REGIAO,NORTH_VIRGINIA_SECURITY_GROUP,'Habilitar portas','django_database',north_virginia_ports_and_protocols)
print()

# ------------------------------------------------------ CRIANDO INSTANCIA EM OHIO ----------------------------------
print("---------------------------------CRIANDO INSTÂNCIA EM OHIO + BANCO DE DADOS---------------------------------")

# CRIANDO BANCO DE DADOS
postgresql, postgresql_public_ip_address, postgresql_instance_id = create_database(POSTGRESQL_REGIAO,POSTGRESQL_IMAGEM,POSTGRESQL_TIPO_INSTANCIA,POSTGRESQL_NOME,POSTGRES_SECURITY_GROUP,KEY_NAME)


# ------------------------------------------------------ North Virginia -----------------------------------------------------------------
print("---------------------------------CRIANDO INTÂNCIA EM NORTH VIRGINIA---------------------------------")

# CRIANDO INSTANCIA
user_data_django = '''#!/bin/bash
cd /
sudo apt update
git clone https://github.com/raulikeda/tasks.git
cd tasks
sudo sed -i s/"'HOST': 'node1',"/"'HOST': '{0}',"/g  portfolio/settings.py
sudo sed -i s/"'PASSWORD': 'cloud',"/"'PASSWORD': '',"/g  portfolio/settings.py
./install.sh
sudo ufw allow 8080/tcp
./run.sh
'''.format(postgresql_public_ip_address)
django, django_ip, django_id = create_instance(NORTH_VIRGINIA_REGIAO,NORTH_VIRGINIA_IMAGEM,NORTH_VIRGINIA_TIPO_INSTANCIA,NORTH_VIRGINIA_NOME,NORTH_VIRGINIA_SECURITYs_GROUP,KEY_NAME,UserData=user_data_django)

# ------------------------------------------------------ AMI -----------------------------------------------------------------
print("-------------------------------------------------CRIANDO AMI-------------------------------------------------")
ami_django, ami_django_id = create_image(north_virginia_client,django_id, 'ami_django',north_virginia_waiter_ami)