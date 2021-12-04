
def get_available_zones(client):
    try:
        response=list()
        available_zones = client.describe_availability_zones()["AvailabilityZones"]
        for zone in available_zones:
            response.append(zone["ZoneName"])
        return response
    except NameError as e:
        print(e)


# REFERENCIAS
#   https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.create_auto_scaling_group

def cria_auto_scaling_group(autoscalling_name, config_name, min_size, max_size, autoscalling_client, region_client, target_group_arns):
    try:
        print("Criando Auto Sacling Group {0}".format(autoscalling_name))
        zones = get_available_zones(region_client)
        autoscalling_client.create_auto_scaling_group(
            AutoScalingGroupName=autoscalling_name,
            LaunchConfigurationName=config_name,
            MinSize=min_size,
            MaxSize=max_size,
            TargetGroupARNs=[target_group_arns],
            AvailabilityZones=zones
        )
        print("Auto Scalling Group {0} criado".format(autoscalling_name))
    except NameError as e:
        print(e)


# REFERENCIAS
#   https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_auto_scaling_group

def deleta_auto_scaling(autoscalling_name, client):
    try:
        print("Deletando Auto Sacling Group {0}".format(client.meta.region_name))
        client.delete_auto_scaling_group(
            AutoScalingGroupName=autoscalling_name,
            ForceDelete=True
        )
        print("Auto Sacling Group {0} deletado".format(client.meta.region_name))
    except:
        print("Auto Sacling Group {0} não encontrado".format(client.meta.region_name))
        pass
