import requests
from requests.auth import HTTPBasicAuth
from functions.utils.create_log import create_log


def get(url, user='cloud', password='cloud'):
    create_log('GET {0}'.format(url))
    response = requests.get(url, auth=HTTPBasicAuth(user, password)).json()
    create_log('GET response {0}'.format(response))
    return response

def post(url, json, end='users', user='cloud', password='cloud'):
    create_log('POST {0}'.format(url))

    if end == 'users':
        response = requests.post(
            url=url,
            auth=HTTPBasicAuth(user, password),
            data={
                "username": json["username"],
                "email": json["email"]
            }
        ).json()

    else:
        response = requests.post(
            url=url,
            auth=HTTPBasicAuth(user, password),
            data={
                "name": json["name"],
            }
        ).json()
    create_log('POST response {0}'.format(response))
    return response

def delete(url, id, user='cloud', password='cloud'):
    create_log('DELETE {0}'.format(url+id))
    response = requests.delete(url=url+id+'/', auth=HTTPBasicAuth(user, password))
    create_log('DELETE response {0}'.format(response))
    return response