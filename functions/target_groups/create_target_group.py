from typing import Protocol
from functions.utils.create_log import create_log


def create_target_group_for_aws(target_group_name,
    protocol, health_check_enabled, health_check_protocol, health_check_port,
    health_check_path, port, target_type, ec2_region, ec2_lb):
    try:
        vpc_id = ec2_region.describe_vpcs()["Vpcs"][0]["VpcId"]
        create_log('Creating target group {0}...'.format(target_group_name))
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
        create_log('Target group {0} created'.format(target_group_name), type='success')
        return target_group["TargetGroups"][0]["TargetGroupArn"]
    except NameError as e:
        create_log(e, type='fail')
