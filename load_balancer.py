
# REFERENCIAS
#   https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_subnets

def mostrar_subnets(ec2):
    current_subnets = ec2.describe_subnets()['Subnets']
    subnet_ids = []
    for subnet in current_subnets:
        subnet_ids.append(subnet['SubnetId'])
    return subnet_ids



# REFERENCIAS
#   https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.create_load_balancer
#   https://www.stratoscale.com/knowledge/load-balancing/aws-elb/boto-3-for-elb/example-work-with-a-load-balancer-and-target-group/


def cria_load_balancer(ec2, lb_client, load_balancer_name, security_group, waiter):
        try:
            subnets=mostrar_subnets(ec2)
            print("Criando Load Balancer {0}".format(load_balancer_name))
            load_balancer = lb_client.create_load_balancer(
                SecurityGroups=[security_group.group_id],
                Tags=[{"Key": "Name", "Value": load_balancer_name}],
                Name=load_balancer_name,
                Subnets=subnets,
                IpAddressType='ipv4',
                Type='application',
                Scheme='internet-facing'
            )
            amazon_resource_name = load_balancer['LoadBalancers'][0]['LoadBalancerArn']
            waiter.wait(LoadBalancerArns=[amazon_resource_name])
            print(" Load Balancer {0} criado".format(load_balancer_name))
            return load_balancer, amazon_resource_name
        except NameError as e:
            print(e)



# REFERENCIAS
#   https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.delete_load_balancer

def deleta_load_balancer(ec2, waiter):
    try:
        current_lb = ec2.describe_load_balancers()['LoadBalancers']
        if len(current_lb) > 0:
            print("Deletando Load balancer")
            for lb in current_lb:
                ec2.delete_load_balancer(LoadBalancerArn=lb['LoadBalancerArn'])
                waiter.wait(LoadBalancerArns=[lb["LoadBalancerArn"]])
            print("Load balancer deletado")
        else:
            print("Não tem Load Balancer para ser deletado")
        return
    except NameError as e:
        print(e)
        return