import boto3
import time
from ami import create_image,delete_image
from autoscalling import cria_auto_scaling_group,deleta_auto_scaling
from instances import create_database,create_instance,terminate_instance
from launch_config import cria_launch_config,deleta_launch_config
from listeners import cria_listener
from load_balancer import cria_load_balancer,deleta_load_balancer
from policies import cria_policy
from security_group import cria_security_group,deleta_security_groups
from target_group import attach_to_load_balancer_for_aws,cria_target_group,deleta_target_group


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

# INITIALIZE LOG FILE ---------------------------------------------
# initialize_log_file('log.txt')

# --------------------------------------------- DELETANDO LOAD BALANCER ---------------------------------------------
deleta_load_balancer(load_balancer_client, load_balancer_waiter_delete)
print()
time.sleep(5)

# --------------------------------------------- DELETANDO AUTO SCALING ---------------------------------------------
deleta_auto_scaling(AT_GROUP_NAME, auto_scalling_client)
print()
time.sleep(5)

# --------------------------------------------- DELETANDO LAUNCH CONFIG ---------------------------------------------
deleta_launch_config(auto_scalling_client, LC_NAME)
print()
time.sleep(5)

# --------------------------------------------- DELETANDO AMIS ---------------------------------------------
delete_image(north_virginia_client)
print()
time.sleep(5)

# --------------------------------------------- DELETANDO INSTÂNCIA---------------------------------------------
terminate_instance(north_virginia_client, north_virginia_waiter_terminate)
terminate_instance(ohio_client, ohio_waiter_terminate)
print()
time.sleep(5)

#--------------------------------------------- DELETANDO TARGET GROUP -------------------------------------------
deleta_target_group(LB_TARGET_GROUP_NAME, load_balancer_client)
print()
time.sleep(5)

# --------------------------------------------- DELETANDO SECURITY GROUPS ---------------------------------------
deleta_security_groups(ohio_client)
deleta_security_groups(north_virginia_client)
print()
time.sleep(5)

# --------------------------------------------- CRIANDO SECURITY GROUPS ----------------------------------------
postgres_protocols = read_command('protocols', 'database_security_group.txt', is_json=True)
postgres_security_group = cria_security_group(
    POSTGRES_SECURITY_GROUP,
   POSTGRES_REGION,
   'enable ports',
   'postgres',
   postgres_protocols)

django_protocols = read_command('protocols', 'django_security_group.txt', is_json=True)
django_security_group = cria_security_group(
   NORTH_VIRGINIA_SECURITY_GROUP,
   NORTH_VIRGINIA_REGION,
   'enable ports',
   'django',
   django_protocols)

load_balancer_protocols = read_command('protocols', 'load_balancer_security_group.txt', is_json=True)
load_balancer_security_group = cria_security_group(
    NORTH_VIRGINIA_SECURITY_GROUP_LD,
    NORTH_VIRGINIA_REGION,
    'enable ports',
    'load_balancer',
    load_balancer_protocols)
print()
time.sleep(5)

# ------------------------------------------------------ CRIANDO INSTANCIA EM OHIO ----------------------------------
postgres, postgres_ip, postgres_id = create_database(
   POSTGRES_NAME,
   POSTGRES_REGION,
   POSTGRES_IMAGE_ID,
   POSTGRES_INSTANCE_TYPE,
   postgres_security_group,
   KEY_NAME)

# ------------------------------------------------------ North Virginia -----------------------------------------------------------------
django_user_data = read_command('commands', 'install_django.sh').replace("s/node1/postgres_ip/g", f"s/node1/{postgres_ip}/g", 1)
django, django_ip, django_id = create_instance(
   NORTH_VIRGINIA_NAME,
   NORTH_VIRGINIA_REGION,
   NORTH_VIRGINIA_IMAGE_ID,
   NORTH_VIRGINIA_INSTANCE_TYPE,
   django_security_group,
   KEY_NAME,
   user_data=django_user_data,
   sleep=True)
print()
time.sleep(5)

# ------------------------------------------------------ AMI -----------------------------------------------------------------
ami_django, ami_django_id = create_image(north_virginia_client, 'django-ami', django_id, north_virginia_waiter_ami)
print()
# ------------------------------------------------------ DELETANDO DJANGO -----------------------------------------------------------------
terminate_instance(north_virginia_client, north_virginia_waiter_terminate)
print()
# ------------------------------------------------------ CRIANDO TARGET GROUP -----------------------------------------------------------------
target_group = cria_target_group(
  LB_TARGET_GROUP_NAME,
  LB_PROTOCOL,
  LB_HEALTH_CHECK_ENABLED,
  LB_HEALTH_CHECK_PROTOCOL,
  LB_HEALTH_CHECK_PORT,
  LB_HEALTH_CHECK_PATH,
  LB_PORT,
  LB_TARGET_TYPE,
  north_virginia_client,
  load_balancer_client)
print()
#------------------------------------------------------ CRIANDO LOAD BALANCER -----------------------------------------------------------------
load_balancer, amazon_resource_name = cria_load_balancer(
    north_virginia_client,
    load_balancer_client,
    'load-balancer-north-viriginia',
    load_balancer_security_group,
    load_balancer_waiter_available)
print()
# ------------------------------------------------------ CRIANDO LAUNCH CONFIG -----------------------------------------------------------------
cria_launch_config(
   auto_scalling_client,
   LC_NAME,
   ami_django_id,
   django_security_group,
   LC_INSTANCE_TYPE,
   KEY_NAME)
print()
#-------------------------------------------------CRIANDO AUTO SCALING-------------------------------------------------
cria_auto_scaling_group(
   AT_GROUP_NAME,
   AT_LAUNCH_CONFIGURATION_NAME,
   AT_MIN_SIZE,
   AT_MAX_SIZE,
   auto_scalling_client,
   north_virginia_client,
   target_group)
print()
# ------------------------------------------------------ ATTACH LOAD BALANCER ------------------------------------------------------
attach_to_load_balancer_for_aws(AT_GROUP_NAME, auto_scalling_client, target_group)
print()
# ------------------------------------------------------ CRIANDO LISTENER -----------------------------------------------------------------
cria_listener(
   LT_PROTOCOL,
   LT_PORT,
   LT_DEFAULT_ACTIONS_TYPE,
   target_group,
   amazon_resource_name,
   load_balancer_client)
print()
# ---------------------------------------------CRIANDO AUTO SCALING POLICY----------------------------------------------
cria_policy(
   POLICY_NAME,
   AT_GROUP_NAME,
   POLICY_TYPE,
   POLICY_TARGET_VALUE,
   POLICY_METRIC_TYPE,
   auto_scalling_client,
   target_group,
   amazon_resource_name
)
print()