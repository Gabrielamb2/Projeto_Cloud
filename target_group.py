
def attach_to_load_balancer_for_aws(auto_scalling_name, ec2, target_group_arn):
    try:
        print('Attaching load balancer to target group...')
        ec2.attach_load_balancer_target_groups(
            AutoScalingGroupName=auto_scalling_name,
            TargetGroupARNs=[target_group_arn]
        )
        print('Load balancer attached!')
    except NameError as e:
        print(e)


# REFERENCIAS
#   https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html

def cria_target_group(target_group_name,
    protocol, health_check_enabled, health_check_protocol, health_check_port,
    health_check_path, port, target_type, ec2_region, ec2_lb):
    try:
        vpc_id = ec2_region.describe_vpcs()["Vpcs"][0]["VpcId"]
        print("Criando Target group {0}".format(target_group_name))
        target_group = ec2_lb.create_target_group(
            Name=target_group_name,
            Protocol=protocol,
            Port=port,
            HealthCheckEnabled=health_check_enabled,
            HealthCheckProtocol=health_check_protocol,
            HealthCheckPort=health_check_port,
            HealthCheckPath=health_check_path,
            Matcher={'HttpCode': '200,302,301,404,403'},
            TargetType=target_type,
            VpcId=vpc_id
        )
        print("Target group {0} criado".format(target_group_name))
        return target_group["TargetGroups"][0]["TargetGroupArn"]
    except NameError as e:
        print(e)




# REFERENCIAS
#   https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.delete_target_group

def deleta_target_group(target_group_name, ec2_load_balancer):
  try:
    print("Deletavdo Target Group")
    current_target_groups = ec2_load_balancer.describe_target_groups()["TargetGroups"]
    if len(current_target_groups) > 0:
      for target_group in current_target_groups:
        if target_group["TargetGroupName"] == target_group_name:
          ec2_load_balancer.delete_target_group(TargetGroupArn=target_group["TargetGroupArn"])
      print("Target Group Deletado")
    else:
        print("Não tem Target Group para deletar")
  except NameError as e:
    print(e)