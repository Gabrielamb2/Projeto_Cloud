import boto3
from botocore.config import Config
from cria_instancia import create_instance

# CONFIGURAÇÃO OHIO
OHIO_NOME='Ohio'
OHIO_REGIAO='us-east-2'
OHIO_IMAGEM='ami-020db2c14939a8efb'
OHIO_TIPO_INSTANCIA='t2.micro'
OHIO_SECURITY_GROUP='test'

# CLIENTE
ohio_client = boto3.client('ec2', region_name=OHIO_REGIAO)

#CRIANDO INSTÂNCIA
ohio = create_instance(OHIO_REGIAO,OHIO_IMAGEM,OHIO_TIPO_INSTANCIA,OHIO_NOME)