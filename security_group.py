import boto3
from botocore.config import Config


# Referências: 
#     https://boto3.amazonaws.com/v1/documentation/api/latest/guide/ec2-example-security-group.html

def cria_security_group(group_name, region, description, tag_name, ports_and_protocols):
    try:
        region = Config(region_name=region)
        resource = boto3.resource('ec2', config=region)
        print('Criando security group: {0}'.format(group_name))
        security_group = resource.create_security_group(
            Description = description, GroupName = group_name,
            TagSpecifications=[{'ResourceType':'security-group',
             'Tags': [{'Key':'Name', 'Value':tag_name}]}]
        )
        for protocol in ports_and_protocols:
            print('Authorizing ingress - IPprotocol: {0}, CirdrIP: {1}, FromPort: {2}, ToPort: {3}'
            .format(protocol['protocol'], protocol['CidrIp'], protocol['FromPort'], protocol['ToPort']))
            security_group.authorize_ingress(
                CidrIp=protocol['CidrIp'],
                FromPort=protocol['FromPort'],
                ToPort=protocol['ToPort'],
                IpProtocol=protocol['protocol'])
        security_group.load()
        print("Security group {0} criado".format(group_name))
        return security_group
    except NameError as e:
        print(e)



# Referências: 
#     https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.delete_security_group
#     https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DeleteSecurityGroup.html

def deleta_security_groups(ec2):
    try:
        print('Deletando instâncias em {0}'.format(ec2.meta.region_name))
        current_security_groups = ec2.describe_security_groups()
        for security_group in current_security_groups["SecurityGroups"]:
            if security_group['GroupName'] != 'default':
                ec2.delete_security_group(GroupId=security_group['GroupId'])
        print('Security groups deletados!')
    except NameError as e:
        print(e)
