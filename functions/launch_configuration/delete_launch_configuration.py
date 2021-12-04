from functions.launch_configuration.check_launch_configuration import check_launch_configuration_for_aws
from functions.utils.create_log import create_log

def delete_launch_configuration_for_aws(ec2, launch_name):
    try:
        create_log('Deleting launch condiguration {0}...'.format(launch_name))
        launch_config_exists = check_launch_configuration_for_aws(launch_name, ec2)
        if launch_config_exists:
            ec2.delete_launch_configuration(LaunchConfigurationName=launch_name)
            create_log('Launch condiguration {0} deleted!'.format(launch_name), type='success')
        else:
            create_log('Launch configuration {0} not found!'.format(launch_name), type='warning')
    except NameError as e:
        create_log(e, type='fail')