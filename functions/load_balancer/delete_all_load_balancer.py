from functions.utils.create_log import create_log

def delete_all_load_balancer_for_aws(ec2, waiter):
    try:
        current_lb = ec2.describe_load_balancers()['LoadBalancers']
        if len(current_lb) > 0:
            create_log('Deleting all loadbalancers...')
            for lb in current_lb:
                ec2.delete_load_balancer(LoadBalancerArn=lb['LoadBalancerArn'])
                waiter.wait(LoadBalancerArns=[lb["LoadBalancerArn"]])
            create_log('All loadbalancers deleted!', type='success')
        else:
            create_log('There are no loadlancers to delete!', type='warning')
        return
    except NameError as e:
        create_log(e, type='fail')
        return