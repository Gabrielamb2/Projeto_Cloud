from functions.utils.create_log import create_log


def delete_autoscalling_for_aws(autoscalling_name, client):
    try:
        create_log('Deleting all autoscalling... ({0})'.format(client.meta.region_name))
        client.delete_auto_scaling_group(
            AutoScalingGroupName=autoscalling_name,
            ForceDelete=True
        )
        create_log('Autoscalling {0} deleted!'.format(client.meta.region_name), type='success')
    except:
        create_log('Autoscalling {0} not found!'.format(client.meta.region_name), type='warning')
        pass
