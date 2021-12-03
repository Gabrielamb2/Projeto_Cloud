# REFERENCIAS
#   https://stackoverflow.com/questions/58227287/how-to-use-boto3-to-create-an-ami-from-an-amazon-ebs-snapshot
#   https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.create_image

def create_image(ec2, ami_name, instance_id, waiter):
    try:
        print("Criando AMI {0}".format(ami_name))
        response = ec2.create_image(
            Name=ami_name,
            InstanceId=instance_id,
            TagSpecifications=[{
                'ResourceType': 'image',
                'Tags': [{'Key': 'Name', 'Value': ami_name}]
            }]
        )
        waiter.wait(ImageIds=[response['ImageId']])
        print("AMI {0} criada".format(ami_name))
        return response, response['ImageId']
    except NameError as e:
        print(e)

# REFERENCIAS
#   https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.deregister_image
#   https://stackoverflow.com/questions/5313726/how-to-delete-an-ami-using-boto

def delete_image(ec2):
    try:
        current_images = ec2.describe_images(Owners=['self'])
        if len(current_images) > 0:
            print("Deletando AMIS")
            for image in current_images['Images']:
                ec2.deregister_image(
                    ImageId=image['ImageId'],
                )
        else:
            print("Não tem AMI para deletar")
    except NameError as e:
        print(e)
