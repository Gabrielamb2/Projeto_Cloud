import boto3
from botocore.config import Config
from instancia import create_instance,terminate_instance
from cria_database import create_database
from security_group import create_security_group,terminate_security_groups
from ami import create_image, delete_image
from load_balancer import cria_load_balancer, deleta_load_balancer,attach_to_load_balancer
from target_group import cria_target_group,deleta_target_group
from launch_configuration import cria_launch_config,deleta_launch_config
from autoscalling import cria_auto_scaling_group, deleta_auto_scaling, cria_listener, cria_scaling
from policy import cria_policy
import json
import time

#AWS KEYS 
KEY_NAME='testeinstancia1'

# CONFIGURAÇÃO POSTGRESQL
POSTGRESQL_NOME='Postgresql'
POSTGRESQL_REGIAO='us-east-2'
POSTGRESQL_IMAGEM='ami-020db2c14939a8efb'
POSTGRESQL_TIPO_INSTANCIA='t2.micro'
POSTGRESQL_SECURITY_GROUP='testePostgres'

# CONFIGURAÇÃO NORTH VIRGINIA
NORTH_VIRGINIA_NOME = 'North-Virigina'
NORTH_VIRGINIA_REGIAO = 'us-east-1'
NORTH_VIRGINIA_IMAGEM = 'ami-0279c3b3186e54acd'
NORTH_VIRGINIA_TIPO_INSTANCIA= 't2.micro'
NORTH_VIRGINIA_SECURITY_GROUP = 'testNorthVirginia'

# CONFIGURAÇÃO LOAD BALANCER
LOAD_BALANCER_SECURITY_GROUP = 'testLoadBalancer'
LOAD_BALANCER_TARGET_GROUP_NAME = 'target-group-b-gabi'
LOAD_BALANCER_PROTOCOLO = 'HTTP'
LOAD_BALANCER_HealthCheckEnabled = True
LOAD_BALANCER_HealthCheckProtocolo = 'HTTP'
LOAD_BALANCER_HealthCheckPorta = '8080'
LOAD_BALANCER_HealthCheckPath = '/admin/'
LOAD_BALANCER_PORTA = 8080
LOAD_BALANCER_TARGET_TYPE = 'instance'


# LAUNCH CONFIGURATION 
LAUNCH_CONFIG_NAME = 'launch_configuration_gabi'
LAUNCH_CONFIG_INSTANCE_TYPE = 't2.micro'

# AUTOSCALLING 
AUTO_SCALiNG_GROUP_NAME = 'auto-scalling-gabi'
AUTO_SCALiNG_LAUNCH_CONFIGURATION_NAME = LAUNCH_CONFIG_NAME
AUTO_SCALiNG_MIN_SIZE = 1
AUTO_SCALiNG_MAX_SIZE = 3
policy_name = 'gabi-target-tracking-scaling-policy'

# LISTENER 
LISTENER_PROTOCOL = 'HTTP'
LISTENER_PORT = 80
LISTENER_DEFAULT_ACTIONS_TYPE = 'forward'

# POLICY
POLICY_NAME = 'auto-scalling-policy'
POLICY_TYPE = 'TargetTrackingScaling'
POLICY_TARGET_VALUE = 50
POLICY_METRIC_TYPE = 'ALBRequestCountPerTarget'

# --------------------------------------------- CLIENTS AND WAITERS ---------------------------------------------
ohio_client = boto3.client('ec2', region_name=POSTGRESQL_REGIAO)
ohio_waiter_terminate = ohio_client.get_waiter('instance_terminated')

north_virginia_client = boto3.client('ec2', region_name=NORTH_VIRGINIA_REGIAO)
north_virginia_waiter_terminate = north_virginia_client.get_waiter('instance_terminated')
north_virginia_waiter_ami = north_virginia_client.get_waiter('image_available')

load_balancer_client = boto3.client('elbv2', region_name=NORTH_VIRGINIA_REGIAO)
load_balancer_waiter_available = load_balancer_client.get_waiter('load_balancer_available')
load_balancer_waiter_delete = load_balancer_client.get_waiter('load_balancers_deleted')

auto_scalling_client = boto3.client('autoscaling', region_name=NORTH_VIRGINIA_REGIAO)


# --------------------------------------------- DELETANDO LOAD BALANCER ---------------------------------------------
deleta_load_balancer(load_balancer_client,load_balancer_waiter_delete)
print()
time.sleep(15)

# --------------------------------------------- DELETANDO AUTO SCALING ---------------------------------------------
deleta_auto_scaling(AUTO_SCALiNG_GROUP_NAME,auto_scalling_client)
print()
time.sleep(15)

# --------------------------------------------- DELETANDO LAUNCH CONFIG ---------------------------------------------
deleta_launch_config(auto_scalling_client,LAUNCH_CONFIG_NAME)
print()
time.sleep(15)

#--------------------------------------------- DELETANDO AMIS ---------------------------------------------
delete_image(north_virginia_client)
print()
time.sleep(15)

# --------------------------------------------- DELETANDO INSTÂNCIA---------------------------------------------
terminate_instance(north_virginia_client, north_virginia_waiter_terminate)
print()
terminate_instance(ohio_client, ohio_waiter_terminate)
print()
time.sleep(15)

#--------------------------------------------- DELETANDO TARGET GROUP -------------------------------------------
deleta_target_group(LOAD_BALANCER_TARGET_GROUP_NAME,load_balancer_client)
print()
time.sleep(15)

# --------------------------------------------- DELETANDO SECURITY GROUPS ---------------------------------------
terminate_security_groups(ohio_client)
print()
terminate_security_groups(north_virginia_client)
print()
time.sleep(15)

# --------------------------------------------- CRIANDO SECURITY GROUPS ----------------------------------------
with open('security_group.txt', 'r') as file:
        postgresql_ports_and_protocols=json.load(file)

POSTGRES_SECURITY_GROUP = create_security_group(POSTGRESQL_REGIAO,POSTGRESQL_SECURITY_GROUP,'Habilitar portas','postgres_databese',postgresql_ports_and_protocols)
print()


with open('django_security_group.txt', 'r') as file:
        north_virginia_ports_and_protocols=json.load(file)

NORTH_VIRGINIA_SECURITYs_GROUP = create_security_group(NORTH_VIRGINIA_REGIAO,NORTH_VIRGINIA_SECURITY_GROUP,'Habilitar portas','django',north_virginia_ports_and_protocols)
print()


with open('load_balancer_security_group.txt', 'r') as file:
        load_balancer_ports_and_protocols=json.load(file)

LOAD_BALANCER_SECURITYs_GROUP = create_security_group(NORTH_VIRGINIA_REGIAO,LOAD_BALANCER_SECURITY_GROUP,'Habilitar portas','load-balancer',load_balancer_ports_and_protocols)
print()
time.sleep(15)

# ------------------------------------------------------ CRIANDO INSTANCIA EM OHIO ----------------------------------
print("---------------------------------CRIANDO INSTÂNCIA EM OHIO + BANCO DE DADOS---------------------------------")

# CRIANDO BANCO DE DADOS
postgresql, postgresql_public_ip_address, postgresql_instance_id = create_database(POSTGRESQL_REGIAO,POSTGRESQL_IMAGEM,POSTGRESQL_TIPO_INSTANCIA,POSTGRESQL_NOME,POSTGRES_SECURITY_GROUP,KEY_NAME)
print()
time.sleep(15)
# ------------------------------------------------------ North Virginia -----------------------------------------------------------------
print("---------------------------------CRIANDO INTÂNCIA EM NORTH VIRGINIA---------------------------------")

# --------------------------------------------- CRIANDO INSTANCIA ---------------------------------------------
user_data_django = '''#!/bin/bash
cd /
sudo apt update
git clone https://github.com/raulikeda/tasks.git
cd tasks
sudo sed -i s/"'HOST': 'node1',"/"'HOST': '{0}',"/g  portfolio/settings.py
sudo sed -i s/"'PASSWORD': 'cloud',"/"'PASSWORD': '',"/g  portfolio/settings.py
./install.sh
sudo ufw allow 8080/tcp
./run.sh
'''.format(postgresql_public_ip_address)
django, django_ip, django_id = create_instance(NORTH_VIRGINIA_REGIAO,NORTH_VIRGINIA_IMAGEM,NORTH_VIRGINIA_TIPO_INSTANCIA,NORTH_VIRGINIA_NOME,NORTH_VIRGINIA_SECURITYs_GROUP,KEY_NAME,UserData=user_data_django,sleep=True)
print()
time.sleep(15)

# ------------------------------------------------------ AMI -----------------------------------------------------------------
print("-------------------------------------------------CRIANDO AMI-------------------------------------------------")
ami_django, ami_django_id = create_image(north_virginia_client, 'ami-django', django_id, north_virginia_waiter_ami)
print()

# ------------------------------------------------------ DELETANDO DJANGO -----------------------------------------------------------------
print("-------------------------------------------------DELETANDO DJANGO-------------------------------------------------")
terminate_instance(north_virginia_client, north_virginia_waiter_terminate)
print()

# ------------------------------------------------------ CRIANDO TARGET GROUP -----------------------------------------------------------------
print("-------------------------------------------------CRIANDO TARGET GROUP-------------------------------------------------")
target_group = cria_target_group(
  LOAD_BALANCER_TARGET_GROUP_NAME,
  LOAD_BALANCER_PROTOCOLO,
  LOAD_BALANCER_HealthCheckEnabled,
  LOAD_BALANCER_HealthCheckProtocolo,
  LOAD_BALANCER_HealthCheckPorta,
  LOAD_BALANCER_HealthCheckPath,
  LOAD_BALANCER_PORTA,
  LOAD_BALANCER_TARGET_TYPE,
  north_virginia_client,
  load_balancer_client)
print()

# ------------------------------------------------------ CRIANDO LOAD BALANCER -----------------------------------------------------------------
print("-------------------------------------------------CRIANDO LOAD BALANCER-------------------------------------------------")
load_balancer, amazon_resource_name, dns = cria_load_balancer(
    north_virginia_client,
    load_balancer_client,
    'load-balancer-NV-gabi',
    LOAD_BALANCER_SECURITYs_GROUP,
    load_balancer_waiter_available)

print("DNS: {0}".format(dns))
print()

# ------------------------------------------------------ CRIANDO LAUNCH CONFIG -----------------------------------------------------------------
print("-------------------------------------------------CRIANDO LAUNCH CONFIG-------------------------------------------------")
cria_launch_config(
   auto_scalling_client,
   LAUNCH_CONFIG_NAME,
   ami_django_id,
   NORTH_VIRGINIA_SECURITYs_GROUP,
   LAUNCH_CONFIG_INSTANCE_TYPE,
   KEY_NAME)
print()

print("-------------------------------------------------CRIANDO AUTO SCALING-------------------------------------------------")
cria_auto_scaling_group(
   AUTO_SCALiNG_GROUP_NAME,
   AUTO_SCALiNG_LAUNCH_CONFIGURATION_NAME,
   AUTO_SCALiNG_MIN_SIZE,
   AUTO_SCALiNG_MAX_SIZE,
   auto_scalling_client,
   north_virginia_client,
   target_group)
print()

# ------------------------------------------------------ ATTACH LOAD BALANCER -----------------------------------------------------------------
print("-------------------------------------------------ATTACH LOAD BALANCER-------------------------------------------------")
attach_to_load_balancer(AUTO_SCALiNG_GROUP_NAME, auto_scalling_client, target_group)
print()

# ------------------------------------------------------ CRIANDO LISTENER -----------------------------------------------------------------
print("-------------------------------------------------CRIANDO LISTENER-------------------------------------------------")
cria_listener(
   LISTENER_PROTOCOL,
   LISTENER_PORT,
   LISTENER_DEFAULT_ACTIONS_TYPE,
   target_group,
   amazon_resource_name,
   load_balancer_client)
print()

print("---------------------------------------------CRIANDO AUTO SCALING POLICY----------------------------------------------")
cria_policy(
   POLICY_NAME,
   AUTO_SCALiNG_GROUP_NAME,
   POLICY_TYPE,
   POLICY_TARGET_VALUE,
   POLICY_METRIC_TYPE,
   auto_scalling_client,
   target_group,
   amazon_resource_name
)
print()


# cria_scaling(load_balancer_client, auto_scalling_client, north_virginia_client,'LOAD-BALANCER-GABI',LOAD_BALANCER_SECURITYs_GROUP, user_data, LAUNCH_CONFIG_NAME, KEY_NAME, AUTO_SCALiNG_GROUP_NAME,policy_name , NORTH_VIRGINIA_NOME, 'TargetGroupGabi')