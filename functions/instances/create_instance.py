import boto3
from botocore.config import Config
import time

from functions.utils.create_log import create_log


def create_instance_for_aws(instance_name, region, image_id, instance_type, security_group, key_name, user_data=None, sleep=False, duration=150):
    try:
        instance_region = Config(region_name=region)
        ec2 = boto3.resource('ec2', config=instance_region)
        create_log("Creating instance {0}...".format(instance_name))
        if user_data:
            instance = ec2.create_instances(ImageId=image_id, MinCount=1, MaxCount=1, InstanceType=instance_type,
                KeyName=key_name, 
                SecurityGroupIds=[security_group.group_id],
                TagSpecifications=[{ "ResourceType": "instance", "Tags": [{"Key": "Name", "Value": instance_name}]}],
                UserData=user_data
            )
        else:
            instance = ec2.create_instances(ImageId=image_id, MinCount=1, MaxCount=1, InstanceType=instance_type,
                KeyName=key_name, 
                SecurityGroupIds=[security_group.group_id],
                TagSpecifications=[{ "ResourceType": "instance", "Tags": [{"Key": "Name", "Value": instance_name}]}],
            )
        instance[0].wait_until_running()
        if sleep:
            create_log('Sleep starting... ({0})'.format(duration))
            time.sleep(duration)
            create_log('Sleep ended')
        instance[0].reload()
        create_log("Instance {0} created!".format(instance_name), type='success')
        return instance, instance[0].public_ip_address, instance[0].instance_id
    except NameError as e:
        create_log(e, type='fail')
        return
