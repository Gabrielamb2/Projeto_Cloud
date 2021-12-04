
def cria_policy(policy_name, auto_scalling_group, policy_type, target_value, predefined_metric_type, ec2, target_group_arn, load_balancer_arn):
    try:
        lb_name = load_balancer_arn[load_balancer_arn.find("app"):]
        tg_name = target_group_arn[target_group_arn.find("targetgroup"):]
        print("Criando Policy {0}".format(policy_name))
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
        print(" Policy {0} criada".format(policy_name))
    except NameError as e:
        print(e)