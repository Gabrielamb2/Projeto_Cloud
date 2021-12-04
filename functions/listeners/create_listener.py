from functions.utils.create_log import create_log


def create_listener_for_aws(protocol, port, default_actions_type, target_group_arn,  load_balancer_arn, ec2):
    try:
        create_log('Creating listener...')
        ec2.create_listener(
            LoadBalancerArn=load_balancer_arn,
            Protocol=protocol,
            Port=port,
            DefaultActions=[{'Type': default_actions_type, 'TargetGroupArn': target_group_arn}]
        )
        create_log('Listener created!', type='success')
    except NameError as e:
        create_log(e, type='fail')
