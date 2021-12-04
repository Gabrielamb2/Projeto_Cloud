def describe_subnets_for_aws(ec2):
    current_subnets = ec2.describe_subnets()['Subnets']
    subnet_ids = []
    for subnet in current_subnets:
        subnet_ids.append(subnet['SubnetId'])
    return subnet_ids