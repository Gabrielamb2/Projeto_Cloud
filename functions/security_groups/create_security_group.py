import boto3
from botocore.config import Config

from functions.utils.create_log import create_log

def create_security_group_for_aws(group_name, region, description, tag_name, ports_and_protocols):
    try:
        region = Config(region_name=region)
        resource = boto3.resource('ec2', config=region)
        create_log('Creating security group {0}...'.format(group_name))
        security_group = resource.create_security_group(
            Description = description, GroupName = group_name,
            TagSpecifications=[{'ResourceType':'security-group',
             'Tags': [{'Key':'Name', 'Value':tag_name}]}]
        )
        for protocol in ports_and_protocols:
            create_log('Authorizing ingress - IPprotocol: {0}, CirdrIP: {1}, FromPort: {2}, ToPort: {3}'
            .format(protocol['protocol'], protocol['CidrIp'], protocol['FromPort'], protocol['ToPort']))
            security_group.authorize_ingress(
                CidrIp=protocol['CidrIp'],
                FromPort=protocol['FromPort'],
                ToPort=protocol['ToPort'],
                IpProtocol=protocol['protocol'])
        security_group.load()
        create_log("Security group {0} created!".format(group_name), type='success')
        return security_group
    except NameError as e:
        create_log(e, type='fail')