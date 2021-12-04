# AWS KEYS ---------------------------------------------
KEY_NAME = 'testeinstancia1'

# NORTH VIRGINIA INSTANCE CONFIG ---------------------------------------------
NORTH_VIRGINIA_NAME = 'North-Virigina-f'
NORTH_VIRGINIA_REGION = 'us-east-1'
NORTH_VIRGINIA_IMAGE_ID = 'ami-0279c3b3186e54acd'
NORTH_VIRGINIA_INSTANCE_TYPE = 't2.micro'
NORTH_VIRGINIA_SECURITY_GROUP = 'django-security-group'
NORTH_VIRGINIA_SECURITY_GROUP_LD = 'load-balancer'

# POSTGRES INSTANCE CONFIG ---------------------------------------------
POSTGRES_NAME = 'Postgres-f'
POSTGRES_REGION = 'us-east-2'
POSTGRES_IMAGE_ID = 'ami-020db2c14939a8efb'
POSTGRES_INSTANCE_TYPE = 't2.micro'
POSTGRES_SECURITY_GROUP = 'database'

# LOAD BALANCER TARGET GROUP ---------------------------------------------
LB_TARGET_GROUP_NAME = 'load-balancer-target-group'
LB_PROTOCOL = 'HTTP'
LB_HEALTH_CHECK_ENABLED = True
LB_HEALTH_CHECK_PROTOCOL = 'HTTP'
LB_HEALTH_CHECK_PORT = '8080'
LB_HEALTH_CHECK_PATH = '/admin/'
LB_PORT = 8080
LB_TARGET_TYPE = 'instance'

# LAUNCH CONFIGURATION ---------------------------------------------
LC_NAME = 'launch_configuration'
LC_INSTANCE_TYPE = 't2.micro'

# AUTOSCALLING ---------------------------------------------
AT_GROUP_NAME = 'auto-scalling'
AT_LAUNCH_CONFIGURATION_NAME = LC_NAME
AT_MIN_SIZE = 1
AT_MAX_SIZE = 3

# LISTENER ---------------------------------------------
LT_PROTOCOL = 'HTTP'
LT_PORT = 80
LT_DEFAULT_ACTIONS_TYPE = 'forward'

# POLICY ---------------------------------------------
POLICY_NAME = 'auto-scalling-policy'
POLICY_TYPE = 'TargetTrackingScaling'
POLICY_TARGET_VALUE = 50
POLICY_METRIC_TYPE = 'ALBRequestCountPerTarget'



