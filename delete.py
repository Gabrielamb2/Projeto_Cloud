import boto3
import time
from ami import create_AMI_for_aws,delete_all_AMIs_for_aws
from autoscalling import create_autoscalling_for_aws,delete_autoscalling_for_aws
from instances import create_database_for_aws,create_instance_for_aws,delete_all_instances_for_aws
from launch_config import create_launch_configuration_for_aws,delete_launch_configuration_for_aws
from listeners import create_listener_for_aws
from load_balancer import create_load_balancer_for_aws,delete_all_load_balancer_for_aws
from policies import create_policy_fow_aws
from security_group import create_security_group_for_aws,delete_all_security_groups_for_aws
from target_group import attach_to_load_balancer_for_aws,create_target_group_for_aws,delete_target_groups_for_aws


from functions.utils.initialize_log_file import initialize_log_file
from functions.utils.read_command import read_command

# AWS KEYS 
KEY_NAME = 'testeinstancia1'

# CONFIGURAÇÃO POSTGRESQL
POSTGRES_NAME = 'Postgresql'
POSTGRES_REGION = 'us-east-2'
POSTGRES_IMAGE_ID = 'ami-020db2c14939a8efb'
POSTGRES_INSTANCE_TYPE = 't2.micro'
POSTGRES_SECURITY_GROUP = 'testePostgres'

# CONFIGURAÇÃO NORTH VIRGINIA 
NORTH_VIRGINIA_NAME = 'North-Virigina'
NORTH_VIRGINIA_REGION = 'us-east-1'
NORTH_VIRGINIA_IMAGE_ID = 'ami-0279c3b3186e54acd'
NORTH_VIRGINIA_INSTANCE_TYPE = 't2.micro'
NORTH_VIRGINIA_SECURITY_GROUP = 'testNorthVirginia'
NORTH_VIRGINIA_SECURITY_GROUP_LD = 'load-balancer'

# CONFIGURAÇÃO LOAD BALANCER
LB_TARGET_GROUP_NAME = 'target-group-b-gabi'
LB_PROTOCOL = 'HTTP'
LB_HEALTH_CHECK_ENABLED = True
LB_HEALTH_CHECK_PROTOCOL = 'HTTP'
LB_HEALTH_CHECK_PORT = '8080'
LB_HEALTH_CHECK_PATH = '/admin/'
LB_PORT = 8080
LB_TARGET_TYPE = 'instance'

# LAUNCH CONFIGURATION 
LC_NAME = 'launch_configuration_gabi'
LC_INSTANCE_TYPE = 't2.micro'

# AUTOSCALLING 
AT_GROUP_NAME = 'auto-scalling-gabi'
AT_LAUNCH_CONFIGURATION_NAME = LC_NAME
AT_MIN_SIZE = 1
AT_MAX_SIZE = 3

# LISTENER 
LT_PROTOCOL = 'HTTP'
LT_PORT = 80
LT_DEFAULT_ACTIONS_TYPE = 'forward'

# POLICY 
POLICY_NAME = 'auto-scalling-policy'
POLICY_TYPE = 'TargetTrackingScaling'
POLICY_TARGET_VALUE = 50
POLICY_METRIC_TYPE = 'ALBRequestCountPerTarget'

# --------------------------------------------- CLIENTS AND WAITERS ---------------------------------------------
ohio_client = boto3.client('ec2', region_name=POSTGRES_REGION)
ohio_waiter_terminate = ohio_client.get_waiter('instance_terminated')

north_virginia_client = boto3.client('ec2', region_name=NORTH_VIRGINIA_REGION)
north_virginia_waiter_terminate = north_virginia_client.get_waiter('instance_terminated')
north_virginia_waiter_ami = north_virginia_client.get_waiter('image_available')

load_balancer_client = boto3.client('elbv2', region_name=NORTH_VIRGINIA_REGION)
load_balancer_waiter_available = load_balancer_client.get_waiter('load_balancer_available')
load_balancer_waiter_delete = load_balancer_client.get_waiter('load_balancers_deleted')

auto_scalling_client = boto3.client('autoscaling', region_name=NORTH_VIRGINIA_REGION)


# --------------------------------------------- DELETANDO LOAD BALANCER ---------------------------------------------
delete_all_load_balancer_for_aws(load_balancer_client, load_balancer_waiter_delete)
print()
time.sleep(5)

# --------------------------------------------- DELETANDO AUTO SCALING ---------------------------------------------
delete_autoscalling_for_aws(AT_GROUP_NAME, auto_scalling_client)
print()
time.sleep(5)

# --------------------------------------------- DELETANDO LAUNCH CONFIG ---------------------------------------------
delete_launch_configuration_for_aws(auto_scalling_client, LC_NAME)
print()
time.sleep(5)

# --------------------------------------------- DELETANDO AMIS ---------------------------------------------
delete_all_AMIs_for_aws(north_virginia_client)
print()
time.sleep(5)

# --------------------------------------------- DELETANDO INSTÂNCIA---------------------------------------------
delete_all_instances_for_aws(north_virginia_client, north_virginia_waiter_terminate)
delete_all_instances_for_aws(ohio_client, ohio_waiter_terminate)
print()
time.sleep(5)

#--------------------------------------------- DELETANDO TARGET GROUP -------------------------------------------
delete_target_groups_for_aws(LB_TARGET_GROUP_NAME, load_balancer_client)
print()
time.sleep(5)

# --------------------------------------------- DELETANDO SECURITY GROUPS ---------------------------------------
delete_all_security_groups_for_aws(ohio_client)
delete_all_security_groups_for_aws(north_virginia_client)
print()
time.sleep(5)
