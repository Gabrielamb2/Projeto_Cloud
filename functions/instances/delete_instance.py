import boto3
from botocore.config import Config

from functions.utils.create_log import create_log

def delete_all_instances_for_aws(ec2, waiter):
    try:
        ids_to_delete = list()
        current_intances = ec2.describe_instances()["Reservations"]
        for instance in current_intances:
            for sub_instance in instance['Instances']:
                if (sub_instance["State"]["Code"] == (0 or 16 or 80)):
                    ids_to_delete.append(sub_instance['InstanceId'])
        if len(ids_to_delete) > 0:
            create_log("Deleting all instances ({0})...".format(ec2.meta.region_name))
            ec2.terminate_instances(InstanceIds=ids_to_delete)
            waiter.wait(InstanceIds=ids_to_delete)
            create_log("All instances deleted!", type='success' )
        else:
            create_log("There are no instances to delete! ({0})".format(ec2.meta.region_name), type='warning')
    except NameError as e:
        create_log(e, type='fail')
