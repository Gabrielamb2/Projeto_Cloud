from functions.utils.create_log import create_log


def create_policy_fow_aws(policy_name, auto_scalling_group, policy_type, target_value, predefined_metric_type, ec2, target_group_arn, load_balancer_arn):
    try:
        create_log('Creating policy {0}...'.format(policy_name))
        lb_name = load_balancer_arn[load_balancer_arn.find("app"):]
        tg_name = target_group_arn[target_group_arn.find("targetgroup"):]
        ec2.put_scaling_policy(
            AutoScalingGroupName=auto_scalling_group,
            PolicyName=policy_name,
            PolicyType=policy_type,
            TargetTrackingConfiguration={
                "PredefinedMetricSpecification": {
                    "PredefinedMetricType": predefined_metric_type,
                    "ResourceLabel": f"{lb_name}/{tg_name}"
                },
                "TargetValue": target_value
            }
        )
        create_log('Policy {0} created!'.format(policy_name), type='success')
    except NameError as e:
        create_log(e, type='fail')
