import boto3
from botocore.config import Config
import time
# Referências: 
#     https://www.learnaws.org/2020/12/16/aws-ec2-boto3-ultimate-guide/
#     https://stackoverflow.com/questions/32863768/how-to-create-an-ec2-instance-using-boto3
#     https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

def create_instance(regiao,imagem,tipo_instancia,nome,grupo_segurnaca,key_name,UserData=None, sleep=False, duration=400):
    try:
        regiao_instancia = Config(region_name=regiao)
        ec2 = boto3.resource('ec2', config=regiao_instancia)
        if UserData:
            print("Criando Instância {0}".format(nome))
            instances = ec2.create_instances(
                ImageId=imagem,
                MinCount=1,
                MaxCount=1,
                InstanceType=tipo_instancia,
                KeyName=key_name,
                SecurityGroupIds=[grupo_segurnaca.group_id],
                TagSpecifications=[{
                    "ResourceType": "instance",
                    "Tags": [{"Key": "Name", "Value": nome}]
                }],
                UserData=UserData
            )
        else:
            print("Criando Instância {0}".format(nome))
            instances = ec2.create_instances(
                ImageId=imagem,
                MinCount=1,
                MaxCount=1,
                InstanceType=tipo_instancia,
                KeyName=key_name,
                SecurityGroupIds=[grupo_segurnaca.group_id],
                TagSpecifications=[{
                    "ResourceType": "instance",
                    "Tags": [{"Key": "Name", "Value": nome}]
                }]
            )
        instances[0].wait_until_running()
        if sleep:
            time.sleep(duration)
            print('Agora vai')
        
        instances[0].reload()
        print("Instância {0} criada ip: {1}".format(nome,instances[0].public_ip_address))
        return instances,instances[0].public_ip_address, instances[0].instance_id
    except NameError as e:
        print(e)
        return 


# Referências: 
#   https://www.learnaws.org/2020/12/16/aws-ec2-boto3-ultimate-guide/

def terminate_instance(ec2,waiter):
    try:
        ids_to_delete = list()
        current_intances = ec2.describe_instances()["Reservations"]
        for instance in current_intances:
            for sub_instance in instance['Instances']:
                if (sub_instance["State"]["Code"] == (0 or 16 or 80)):
                    ids_to_delete.append(sub_instance['InstanceId'])
        if len(ids_to_delete) > 0:
            print("Deletando instâncias em {0}".format(ec2.meta.region_name))
            response = ec2.terminate_instances(InstanceIds=ids_to_delete)
            waiter.wait(InstanceIds=ids_to_delete)
            print("Instância {0} terminada".format(response['TerminatingInstances'][0]['InstanceId']))
        else:
            print("Não tem instâncias para deletar em {0}".format(ec2.meta.region_name))
    except NameError as e:
        print(e)
