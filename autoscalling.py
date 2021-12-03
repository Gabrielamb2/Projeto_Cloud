# REFERENCIAS
#   https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.create_auto_scaling_group
import boto3

def get_available_zones(client):
    try:
        response=list()
        zonas_acessivel = client.describe_availability_zones()["AvailabilityZones"]
        for zona in zonas_acessivel:
            response.append(zona["ZoneName"])
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
        print("Auto Sacling Group {0} criado".format(autoscalling_name))
        
    except NameError as e:
        print(e)

# REFERENCIAS
#   https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_auto_scaling_group

def deleta_auto_scaling(autoscalling_name, client):
    try:
        print("Deletando Auto Sacling Group {0}".format(autoscalling_name))
        client.delete_auto_scaling_group(
            AutoScalingGroupName=autoscalling_name,
            ForceDelete=True
        )
        print("Auto Sacling Group {0} deletado".format(autoscalling_name))
    except:
        
        pass


# REFERENCIAS
#   https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.create_listener

def cria_listener(protocol, port, default_actions_type, target_group_arn,  load_balancer_arn, ec2):
    try:
        print("Criando Listener")
        ec2.create_listener(
            LoadBalancerArn=load_balancer_arn,
            Protocol=protocol,
            Port=port,
            DefaultActions=[{'Type': default_actions_type, 'TargetGroupArn': target_group_arn}]
        )
        print("Listener Criado")
    except NameError as e:
        print(e)



def cria_scaling(lb_client, autoscalling_client, ec2_nv, lb_nome, sc_lb, user_data_nv, launch_config_nv, KeyName, asg_nome, policy_name_nv, tag_nv, tg_nome):

    try:

        subnet_list = ec2_nv.describe_subnets()
        vpc_list_nv = ec2_nv.describe_vpcs()
        vpc_nv = vpc_list_nv['Vpcs'][0]['VpcId']    
        subnets = []
        for sn in subnet_list['Subnets']:
            subnets.append(sn['SubnetId'])

        create_lb_response = lb_client.create_load_balancer(Name=lb_nome,
                                                             Subnets=subnets,
                                                             SecurityGroups=[
                                                                 sc_lb],
                                                             Scheme='internet-facing')

        lbId = create_lb_response['LoadBalancers'][0]['LoadBalancerArn']
        print('Load Balancer criado com sucesso')
        

        print('Criando grupos de Destino')
        

        create_tg = lb_client.create_target_group(Name=tg_nome,
                                                   Protocol='HTTP',
                                                   Port=8080,
                                                   VpcId=vpc_id)

        tgId = create_tg['TargetGroups'][0]['TargetGroupArn']

        print('Criando Listener')
        

        create_listener_response = lb_client.create_listener(LoadBalancerArn=lbId,
                                                              Protocol='HTTP', Port=80,
                                                              DefaultActions=[{'Type': 'forward',
                                                                               'TargetGroupArn': tgId}])

        get_image_id = ec2_nv.describe_images(Owners=['self'])
        imageId = get_image_id['Images'][0]['ImageId']

        print('Criando Launch Configuration')
        

        launch_config = autoscalling_client.create_launch_configuration(
            LaunchConfigurationName=launch_config_nv,
            ImageId=imageId,
            KeyName=KeyName,
            UserData=user_data_nv,
            SecurityGroups=[sc_lb],
            InstanceType='t2.micro'
        )

        print('Criando Autoscaling')
        

        auto_scaling_Nv = autoscalling_client.create_auto_scaling_group(
            AutoScalingGroupName=asg_nome,
            LaunchConfigurationName=launch_config_nv,
            TargetGroupARNs=[tgId],
            MaxInstanceLifetime=2592000,
            MaxSize=3,
            MinSize=1,
            VPCZoneIdentifier=subnets[4],
            Tags=[
                {
                    "Key": "Name",
                    "Value": tag_nv,
                    "PropagateAtLaunch": True
                }
            ]
        )

        cmd_res_label = 'a' + lbId.split('/a')[1] + '/t' + tgId.split(':t')[1]

        response = autoscalling_client.put_scaling_policy(
            AutoScalingGroupName=asg_nome,
            PolicyName=policy_name_nv,
            PolicyType='TargetTrackingScaling',
            TargetTrackingConfiguration={
                'PredefinedMetricSpecification': {
                    'PredefinedMetricType': 'ALBRequestCountPerTarget',
                    'ResourceLabel': cmd_res_label,
                },
                'TargetValue': 50.0,
            },
        )

        print('Autoscaling criado com sucesso')
        

    except Exception as e:
        print(e)
        

    return "Escalabilidade realizada com sucesso!"