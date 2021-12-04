from functions.utils.create_log import create_log

def create_AMI_for_aws(ec2, ami_name, instance_id, waiter):
    try:
        create_log('Creating AMI {0}...'.format(ami_name))
        ami = ec2.create_image(
            Name=ami_name,
            InstanceId=instance_id,
            TagSpecifications=[{
                'ResourceType': 'image',
                'Tags': [{'Key': 'Name', 'Value': ami_name}]
            }]
        )
        waiter.wait(ImageIds=[ami['ImageId']])
        create_log('AMI {0} created!'.format(ami_name), type='success')
        return ami, ami['ImageId']
    except NameError as e:
        create_log(e, type='fail')

