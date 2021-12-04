from functions.utils.create_log import create_log

def delete_target_groups_for_aws(target_group_name, ec2_load_balancer):
  try:
    create_log('Deleting target group {0}...'.format(target_group_name))
    current_target_groups = ec2_load_balancer.describe_target_groups()["TargetGroups"]
    if len(current_target_groups) > 0:
      for target_group in current_target_groups:
        if target_group["TargetGroupName"] == target_group_name:
          ec2_load_balancer.delete_target_group(TargetGroupArn=target_group["TargetGroupArn"])
      create_log('Target group {0} deleted!'.format(target_group_name), type='success')
    else:
        create_log("Target group {0} doesn't exists", type='warning')
  except NameError as e:
    create_log(e, type='fail')