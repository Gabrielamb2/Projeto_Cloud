import boto3
from botocore.config import Config
from functions.utils.read_command import read_command
import time


# Referências: 
#     https://stackoverflow.com/questions/3777301/how-to-call-a-shell-script-from-python-code/3777351

def create_database(instance_name, region, image_id, instance_type, security_group, key_name):
    print("Criando Database {0}".format(instance_name))
    commands = read_command('commands','install_postgres.sh')
    postgres, postgres_ip, postgres_id = create_instance_for_aws(instance_name, region, image_id, instance_type, security_group, key_name, user_data=commands)
    print("Database {0} criado".format(instance_name))
    return postgres, postgres_ip, postgres_id


# Referências: 
#     https://www.learnaws.org/2020/12/16/aws-ec2-boto3-ultimate-guide/
#     https://stackoverflow.com/questions/32863768/how-to-create-an-ec2-instance-using-boto3
#     https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

def create_instance(instance_name, region, image_id, instance_type, security_group, key_name, user_data=None, sleep=False, duration=150):
    try:
        instance_region = Config(region_name=region)
        ec2 = boto3.resource('ec2', config=instance_region)
        if user_data:
            print("Criando Instância {0}".format(instance_name))
            instance = ec2.create_instances(ImageId=image_id, MinCount=1, MaxCount=1, InstanceType=instance_type,
                KeyName=key_name, 
                SecurityGroupIds=[security_group.group_id],
                TagSpecifications=[{ "ResourceType": "instance", "Tags": [{"Key": "Name", "Value": instance_name}]}],
                UserData=user_data
            )
        else:
            print("Criando Instância {0}".format(instance_name))
            instance = ec2.create_instances(ImageId=image_id, MinCount=1, MaxCount=1, InstanceType=instance_type,
                KeyName=key_name, 
                SecurityGroupIds=[security_group.group_id],
                TagSpecifications=[{ "ResourceType": "instance", "Tags": [{"Key": "Name", "Value": instance_name}]}],
            )
        instance[0].wait_until_running()
        if sleep:
            time.sleep(duration)
            print('Agora vai')
        instance[0].reload()
        print("Instância {0} criada ip: {1}".format(instance_name,instance[0].public_ip_address))
        return instance, instance[0].public_ip_address, instance[0].instance_id
    except NameError as e:
        print(e)
        return



# Referências: 
#   https://www.learnaws.org/2020/12/16/aws-ec2-boto3-ultimate-guide/

def terminate_instance(ec2, waiter):
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
