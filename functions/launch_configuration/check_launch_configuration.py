def check_launch_configuration_for_aws(launch_config_name, ec2):
    current_configs = ec2.describe_launch_configurations()['LaunchConfigurations']
    for config in current_configs:
        if config['LaunchConfigurationName'] == launch_config_name:
            return True
    return False