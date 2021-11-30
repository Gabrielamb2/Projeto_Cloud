import boto3
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
            print("Deletando Security Group em {0}".format(ec2.meta.region_name))
            response = ec2.terminate_instances(InstanceIds=ids_to_delete)
            waiter.wait(InstanceIds=ids_to_delete)
            print("Instância {0} terminada".format(response['TerminatingInstances'][0]['InstanceId']))
        else:
            print("Não tem instâncias para deletar em {0}".format(ec2.meta.region_name))
    except NameError as e:
        print(e)

