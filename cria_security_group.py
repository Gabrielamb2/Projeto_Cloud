import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

# Referências: 
#     https://boto3.amazonaws.com/v1/documentation/api/latest/guide/ec2-example-security-group.html

def create_security_group(regiao,nome_grupo,descricao,tag_name,ports_and_protocols):
    
    try:
        region = Config(region_name=regiao)
        resource = boto3.resource('ec2', config=region)
        print('Criando security group: {0}'.format(nome_grupo))
        security_group = resource.create_security_group(
            Description = descricao, GroupName = nome_grupo,
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
        print("Security group {0} criado".format(nome_grupo))
        return security_group
    except NameError as e:
        print(e)