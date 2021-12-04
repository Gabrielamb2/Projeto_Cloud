import boto3
from botocore.config import Config
from functions.instances.create_instance import create_instance_for_aws
from functions.utils.read_command import read_command
from functions.utils.create_log import create_log

def create_database_for_aws(instance_name, region, image_id, instance_type, security_group, key_name):
    commands = read_command('commands','install_postgres.sh')
    postgres, postgres_ip, postgres_id = create_instance_for_aws(instance_name, region, image_id, instance_type, security_group, key_name, user_data=commands)
    create_log('Database created with postgres!', type='success')
    return postgres, postgres_ip, postgres_id