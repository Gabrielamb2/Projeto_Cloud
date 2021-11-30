import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

# Referências: 
#     https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.delete_security_group
#     https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteSecurityGroup.html

def terminate_security_groups(ec2):
    try:
        print('Deletando instâncias em {0}'.format(ec2.meta.region_name))
        current_security_groups = ec2.describe_security_groups()
        for security_group in current_security_groups["SecurityGroups"]:
            if security_group['GroupName'] != 'default':
                ec2.delete_security_group(GroupId=security_group['GroupId'])
        print('Security groups deletados!')
    except NameError as e:
        print(e)