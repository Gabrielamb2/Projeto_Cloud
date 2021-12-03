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

# --------------------------------------------- CLIENTS AND WAITERS ---------------------------------------------
ohio_client = boto3.client('ec2', region_name=POSTGRESQL_REGIAO)
ohio_waiter_terminate = ohio_client.get_waiter('instance_terminated')

north_virginia_client = boto3.client('ec2', region_name=NORTH_VIRGINIA_REGIAO)
north_virginia_waiter_terminate = north_virginia_client.get_waiter('instance_terminated')

north_virginia_waiter_ami = north_virginia_client.get_waiter('image_available')

load_balancer_client = boto3.client('elbv2', region_name=NORTH_VIRGINIA_REGIAO)
load_balancer_waiter_available = load_balancer_client.get_waiter('load_balancer_available')
load_balancer_waiter_delete = load_balancer_client.get_waiter('load_balancers_deleted')

# --------------------------------------------- DELETANDO LOAD BALANCER ---------------------------------------------
deleta_load_balancer(load_balancer_client,load_balancer_waiter_delete)
print()

# --------------------------------------------- DELETANDO INSTÂNCIA---------------------------------------------
terminate_instance(ohio_client, ohio_waiter_terminate)
print()
terminate_instance(north_virginia_client, north_virginia_waiter_terminate)
print()

#--------------------------------------------- DELETANDO AMIS ---------------------------------------------
delete_image(north_virginia_client)
print()
delete_image(ohio_client)
print()

#--------------------------------------------- DELETANDO TARGET GROUP ---------------------------------------------
deleta_target_group(load_balancer_client)


# --------------------------------------------- DELETANDO SECURITY GROUPS ---------------------------------------------
terminate_security_groups(ohio_client)
print()
terminate_security_groups(north_virginia_client)
print()
