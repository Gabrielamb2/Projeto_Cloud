import boto3
from botocore.config import Config
from cria_instancia import create_instance

# Referências: 
#     https://stackoverflow.com/questions/3777301/how-to-call-a-shell-script-from-python-code/3777351

def create_database(regiao,imagem,tipo_instancia,nome,grupo_segurnaca,key_name):
    #ler o arquivo
    with open('instalar_postgresql.sh', 'r') as file:
        arquivo = file.read()
    instancia = create_instance(regiao,imagem,tipo_instancia,nome,grupo_segurnaca,key_name,UserData=arquivo)
    print("Database criado com postgres")
    return instancia