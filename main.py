import boto3
from botocore.config import Config
from cria_instancia import create_instance
from cria_database import create_database

#AWS KEYS 
KEY_NAME='gabrielamb2'

# CONFIGURAÇÃO OHIO
OHIO_NOME='Ohio'
OHIO_REGIAO='us-east-2'
OHIO_IMAGEM='ami-020db2c14939a8efb'
OHIO_TIPO_INSTANCIA='t2.micro'
OHIO_SECURITY_GROUP='teste'

# CONFIGURAÇÃO POSTGRESQL
POSTGRESQL_NOME='Postgresql'
POSTGRESQL_REGIAO='us-east-2'
POSTGRESQL_IMAGEM='ami-020db2c14939a8efb'
POSTGRESQL_TIPO_INSTANCIA='t2.micro'
POSTGRESQL_SECURITY_GROUP='teste'

# CLIENTE
ohio_client = boto3.client('ec2', region_name=OHIO_REGIAO)

# CRIANDO INSTÂNCIA
# ohio = create_instance(OHIO_REGIAO,OHIO_IMAGEM,OHIO_TIPO_INSTANCIA,OHIO_NOME)

# CRIANDO BANCO DE DADOS
postgresql = create_database(POSTGRESQL_REGIAO,POSTGRESQL_IMAGEM,POSTGRESQL_TIPO_INSTANCIA,POSTGRESQL_NOME,POSTGRESQL_SECURITY_GROUP,KEY_NAME)