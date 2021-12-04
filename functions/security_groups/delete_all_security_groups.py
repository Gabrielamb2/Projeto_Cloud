from functions.utils.create_log import create_log

def delete_all_security_groups_for_aws(ec2):
    try:
        create_log('Deleting all security groups ({0})...'.format(ec2.meta.region_name))
        current_security_groups = ec2.describe_security_groups()
        for security_group in current_security_groups["SecurityGroups"]:
            if security_group['GroupName'] != 'default':
                ec2.delete_security_group(GroupId=security_group['GroupId'])
        create_log('All security groups deleted!', type='success')
    except NameError as e:
        create_log(e, type='fail')
