import boto3
from botocore.config import Config

# Referências: 
#     https://www.learnaws.org/2020/12/16/aws-ec2-boto3-ultimate-guide/
#     https://stackoverflow.com/questions/32863768/how-to-create-an-ec2-instance-using-boto3
#     https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

def create_instance(regiao,imagem,tipo_instancia,nome,grupo_segurnaca,key_name,UserData=None):
    try:
        regiao_instancia = Config(region_name=regiao)
        ec2 = boto3.resource('ec2', config=regiao_instancia)
        if UserData:
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
        print("Instância {} criada!".format(nome))
        return instances, instances[0].public_ip_address, instances[0].instance_id
    except NameError as e:
        print(e)
        return 