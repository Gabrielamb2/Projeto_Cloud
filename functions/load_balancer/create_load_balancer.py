from functions.utils.create_log import create_log
from functions.subnets.describe_subnets import describe_subnets_for_aws

def create_load_balancer_for_aws(ec2, lb_client, load_balancer_name, security_group, waiter):
        try:
            create_log('Creating loadbalancer {0}'.format(load_balancer_name))
            subnets=describe_subnets_for_aws(ec2)
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
            create_log('Loadbalancer {0} created!'.format(load_balancer_name), type='success')
            return load_balancer, amazon_resource_name
        except NameError as e:
            create_log(e, type='fail')

