from functions.utils.create_log import create_log

def get_available_zones_for_aws(client):
    try:
        response=list()
        available_zones = client.describe_availability_zones()["AvailabilityZones"]
        for zone in available_zones:
            response.append(zone["ZoneName"])
        return response
    except NameError as e:
        create_log(e)