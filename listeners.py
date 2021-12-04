

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
