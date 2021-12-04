from functions.utils.create_log import create_log
from functions.utils.get_available_zones import get_available_zones_for_aws


def create_autoscalling_for_aws(autoscalling_name, config_name, min_size, max_size, autoscalling_client, region_client, target_group_arns):
    try:
        create_log('Creating autoscalling {0}...'.format(autoscalling_name))
        zones = get_available_zones_for_aws(region_client)
        autoscalling_client.create_auto_scaling_group(
            AutoScalingGroupName=autoscalling_name,
            LaunchConfigurationName=config_name,
            MinSize=min_size,
            MaxSize=max_size,
            TargetGroupARNs=[target_group_arns],
            AvailabilityZones=zones
        )
        create_log('Autoscalling {0} created!'.format(autoscalling_name), type='success')
    except NameError as e:
        create_log(e, type='fail')
