from functions.utils.create_log import create_log

def delete_all_AMIs_for_aws(ec2):
    try:
        current_images = ec2.describe_images(Owners=['self'])
        if len(current_images) > 0:
            create_log('Deleting all images ({0})...'.format(ec2.meta.region_name))
            for image in current_images['Images']:
                ec2.deregister_image(ImageId=image['ImageId'])
            create_log('All images deleted! ({0})'.format(ec2.meta.region_name), type='success')
        else:
            create_log("There are no AMIs to delete! ({0})".format(ec2.meta.region_name), type='warning')
    except NameError as e:
        create_log(e)
