from functions.utils.create_log import create_log

def attach_to_load_balancer_for_aws(auto_scalling_name, ec2, target_group_arn):
    try:
        create_log('Attaching load balancer to target group...')
        ec2.attach_load_balancer_target_groups(
            AutoScalingGroupName=auto_scalling_name,
            TargetGroupARNs=[target_group_arn]
        )
        create_log('Load balancer attached!', type='success')
    except NameError as e:
        create_log(e, type='fail')
