from functions.utils.create_log import create_log

def create_launch_configuration_for_aws(ec2, launch_name, image_id, security_group, instance_type, key_name):
    try:
        create_log('Creating {0} launch configuration'.format(launch_name))
        ec2.create_launch_configuration(
            LaunchConfigurationName=launch_name,
            ImageId=image_id,
            SecurityGroups=[security_group.group_id],
            InstanceType=instance_type,
            KeyName=key_name
        )
        create_log('Launch configuration {0} created!'.format(launch_name), type='success')
    except NameError as e:
        create_log(e, type='fail')