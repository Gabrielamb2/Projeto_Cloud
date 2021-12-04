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
from read_command import *

# AWS KEYS 
KEY_NAME = 'testeinstancia1'

# CONFIGURAÇÃO POSTGRESQL
POSTGRESQL_NOME = 'Postgresql'
POSTGRESQL_REGIAO = 'us-east-2'
POSTGRESQL_IMAGEM = 'ami-020db2c14939a8efb'
POSTGRESQL_TIPO_INSTANCIA = 't2.micro'
POSTGRESQL_SECURITY_GROUP = 'testePostgres'

# CONFIGURAÇÃO NORTH VIRGINIA 
NORTH_VIRGINIA_NOME  = 'North-Virigina'
NORTH_VIRGINIA_REGIAO  = 'us-east-1'
NORTH_VIRGINIA_IMAGEM  = 'ami-0279c3b3186e54acd'
NORTH_VIRGINIA_TIPO_INSTANCIA = 't2.micro'
NORTH_VIRGINIA_SECURITY_GROUP = 'testNorthVirginia'
NORTH_VIRGINIA_SECURITY_GROUP_LD = 'load-balancer'

# CONFIGURAÇÃO LOAD BALANCER
LOAD_BALANCER_TARGET_GROUP_NAME  = 'target-group-b-gabi'
LOAD_BALANCER_PROTOCOLO  = 'HTTP'
LOAD_BALANCER_HEALTH_CHECK_ENABLED = True
LOAD_BALANCER_HEALTH_CHECK_PROTOCOL = 'HTTP'
LOAD_BALANCER_HEALTH_CHECK_PORT = '8080'
LOAD_BALANCER_HEALTH_CHECK_PATH = '/admin/'
LOAD_BALANCER_PORT = 8080
LOAD_BALANCER_TARGET_TYPE = 'instance'

# LAUNCH CONFIGURATION 
LAUNCH_CONFIG_NAME  = 'launch_configuration_gabi'
LAUNCH_CONFIG_INSTANCE_TYPE = 't2.micro'

# AUTOSCALLING 
AUTO_SCALING_GROUP_NAME  = 'auto-scalling-gabi'
AUTO_SCALING_LAUNCH_CONFIGURATION_NAME = LAUNCH_CONFIG_NAME 
AUTO_SCALING_MIN_SIZE = 1
AUTO_SCALING_MAX_SIZE = 3

# LISTENER 
LISTENER_PROTOCOL  = 'HTTP'
LISTENER_PORT  = 80
LISTENER_DEFAULT_ACTIONS_TYPE  = 'forward'

# POLICY 
POLICY_NAME = 'auto-scalling-policy'
POLICY_TYPE = 'TargetTrackingScaling'
POLICY_TARGET_VALUE = 50
POLICY_METRIC_TYPE = 'ALBRequestCountPerTarget'

# --------------------------------------------- CLIENTS AND WAITERS ---------------------------------------------
ohio_client = boto3.client('ec2', region_name=POSTGRESQL_REGIAO)
ohio_waiter_terminate = ohio_client.get_waiter('instance_terminated')

north_virginia_client = boto3.client('ec2', region_name=NORTH_VIRGINIA_REGIAO )
north_virginia_waiter_terminate = north_virginia_client.get_waiter('instance_terminated')
north_virginia_waiter_ami = north_virginia_client.get_waiter('image_available')

load_balancer_client = boto3.client('elbv2', region_name=NORTH_VIRGINIA_REGIAO )
load_balancer_waiter_available = load_balancer_client.get_waiter('load_balancer_available')
load_balancer_waiter_delete = load_balancer_client.get_waiter('load_balancers_deleted')

auto_scalling_client = boto3.client('autoscaling', region_name=NORTH_VIRGINIA_REGIAO )

# --------------------------------------------- DELETANDO LOAD BALANCER ---------------------------------------------
deleta_load_balancer(load_balancer_client, load_balancer_waiter_delete)
print()
time.sleep(5)

# --------------------------------------------- DELETANDO AUTO SCALING ---------------------------------------------
deleta_auto_scaling(AUTO_SCALING_GROUP_NAME, auto_scalling_client)
print()
time.sleep(5)

# --------------------------------------------- DELETANDO LAUNCH CONFIG ---------------------------------------------
deleta_launch_config(auto_scalling_client, LAUNCH_CONFIG_NAME )
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
deleta_target_group(LOAD_BALANCER_TARGET_GROUP_NAME , load_balancer_client)
print()
time.sleep(5)

# --------------------------------------------- DELETANDO SECURITY GROUPS ---------------------------------------
deleta_security_groups(ohio_client)
deleta_security_groups(north_virginia_client)
print()
time.sleep(5)

# --------------------------------------------- CRIANDO SECURITY GROUPS ----------------------------------------
postgres_protocols = read_command('security_group', 'database_security_group.txt', is_json=True)
postgres_security_group = cria_security_group(POSTGRESQL_SECURITY_GROUP,POSTGRESQL_REGIAO,'enable ports','postgres',postgres_protocols)

django_protocols = read_command('security_group', 'django_security_group.txt', is_json=True)
django_security_group = cria_security_group(NORTH_VIRGINIA_SECURITY_GROUP,NORTH_VIRGINIA_REGIAO ,'enable ports','django',django_protocols)

load_balancer_protocols = read_command('security_group', 'load_balancer_security_group.txt', is_json=True)
load_balancer_security_group = cria_security_group(NORTH_VIRGINIA_SECURITY_GROUP_LD, NORTH_VIRGINIA_REGIAO ,'enable ports','load_balancer',load_balancer_protocols)
print()
time.sleep(5)

# ------------------------------------------------------ CRIANDO INSTANCIA EM OHIO ----------------------------------
postgres, postgres_ip, postgres_id = create_database(POSTGRESQL_NOME,POSTGRESQL_REGIAO,POSTGRESQL_IMAGEM,POSTGRESQL_TIPO_INSTANCIA,postgres_security_group, KEY_NAME)
print()
# ------------------------------------------------------ North Virginia -----------------------------------------------------------------
django_user_data = read_command('instalation', 'install_django.sh').replace("s/node1/postgres_ip/g", f"s/node1/{postgres_ip}/g", 1)
django, django_ip, django_id = create_instance(NORTH_VIRGINIA_NOME ,NORTH_VIRGINIA_REGIAO ,NORTH_VIRGINIA_IMAGEM ,NORTH_VIRGINIA_TIPO_INSTANCIA,django_security_group,KEY_NAME,user_data=django_user_data,sleep=True)
print()
time.sleep(5)

# ------------------------------------------------------ AMI -----------------------------------------------------------------
ami_django, ami_django_id = create_image(north_virginia_client, 'django-ami', django_id, north_virginia_waiter_ami)
print()

# ------------------------------------------------------ DELETANDO DJANGO -----------------------------------------------------------------
terminate_instance(north_virginia_client, north_virginia_waiter_terminate)
print()

# ------------------------------------------------------ CRIANDO TARGET GROUP -----------------------------------------------------------------
target_group = cria_target_group(LOAD_BALANCER_TARGET_GROUP_NAME ,LOAD_BALANCER_PROTOCOLO ,LOAD_BALANCER_HEALTH_CHECK_ENABLED,LOAD_BALANCER_HEALTH_CHECK_PROTOCOL,LOAD_BALANCER_HEALTH_CHECK_PORT,LOAD_BALANCER_HEALTH_CHECK_PATH,LOAD_BALANCER_PORT,LOAD_BALANCER_TARGET_TYPE,north_virginia_client,load_balancer_client)
print()

#------------------------------------------------------ CRIANDO LOAD BALANCER -----------------------------------------------------------------
load_balancer, amazon_resource_name = cria_load_balancer(north_virginia_client,load_balancer_client,'lb-north-virginia-G',load_balancer_security_group,load_balancer_waiter_available)
print()

# ------------------------------------------------------ CRIANDO LAUNCH CONFIG -----------------------------------------------------------------
cria_launch_config(auto_scalling_client,LAUNCH_CONFIG_NAME ,ami_django_id,django_security_group,LAUNCH_CONFIG_INSTANCE_TYPE,KEY_NAME)
print()

#-------------------------------------------------CRIANDO AUTO SCALING-------------------------------------------------
cria_auto_scaling_group(AUTO_SCALING_GROUP_NAME, AUTO_SCALING_LAUNCH_CONFIGURATION_NAME,AUTO_SCALING_MIN_SIZE,AUTO_SCALING_MAX_SIZE,auto_scalling_client,north_virginia_client,target_group)
print()

# ------------------------------------------------------ ATTACH LOAD BALANCER ------------------------------------------------------
attach_to_load_balancer_for_aws(AUTO_SCALING_GROUP_NAME, auto_scalling_client, target_group)
print()

# ------------------------------------------------------ CRIANDO LISTENER -----------------------------------------------------------------
cria_listener(LISTENER_PROTOCOL ,LISTENER_PORT ,LISTENER_DEFAULT_ACTIONS_TYPE ,target_group,amazon_resource_name,load_balancer_client)
print()

# ---------------------------------------------CRIANDO AUTO SCALING POLICY----------------------------------------------
cria_policy(POLICY_NAME,AUTO_SCALING_GROUP_NAME,POLICY_TYPE,POLICY_TARGET_VALUE,POLICY_METRIC_TYPE,auto_scalling_client,target_group,amazon_resource_name)
