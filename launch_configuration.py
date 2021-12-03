# REFERENCIAS
#   https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_launch_configurations

def descreve_launch_config(launch_config_name,ec2):
    current_configs = ec2.describe_launch_configurations()['LaunchConfigurations']
    for config in current_configs:
        if config['LaunchConfigurationName'] == launch_config_name:
            return True
    return False

# REFERENCIAS
#   https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.create_launch_configuration

def cria_launch_config(ec2, launch_name, image_id, security_group, instance_type, key_name):
    try:
        print("Criando Configuração para Launch")
        ec2.create_launch_configuration(
            LaunchConfigurationName=launch_name,
            ImageId=image_id,
            SecurityGroups=[security_group.group_id],
            InstanceType=instance_type,
            KeyName=key_name
        )
        print("Configuração para Launch {0} criado".format(launch_name))
    except NameError as e:
        print(e)


# REFERENCIAS
#   https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_launch_configuration

def deleta_launch_config(ec2, launch_name):
    try:
        launch_config_exists = descreve_launch_config(launch_name, ec2)
        if launch_config_exists:
            print("Deletando Launch Configuration {0}".format(launch_name))
            ec2.delete_launch_configuration(LaunchConfigurationName=launch_name)
            print("Launch Configuration {0} deletado".format(launch_name))
        else:
            print("Launch Configuration {0} não encontrado".format(launch_name))
    except NameError as e:
        print(e)