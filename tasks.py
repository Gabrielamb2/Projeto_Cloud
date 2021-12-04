import requests
from requests.auth import HTTPBasicAuth


def get(url, user='cloud', password='cloud'):
    print('GET {0}'.format(url))
    response = requests.get(url, auth=HTTPBasicAuth(user, password)).json()
    print('GET resposta: {0}'.format(response))
    return response

def post(url, json, end='users', user='cloud', password='cloud'):
    print('POST {0}'.format(url))

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
    print('POST resposta: {0}'.format(response))
    return response

def delete(url, id, user='cloud', password='cloud'):
    print('DELETE {0}'.format(url+id))
    response = requests.delete(url=url+id+'/', auth=HTTPBasicAuth(user, password))
    print('DELETE resposta: {0}'.format(response))
    return response