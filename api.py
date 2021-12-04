from datetime import datetime

import json
from functions.utils.create_log import create_log
from endpoints import tasks

dns = input('url: ')
url = "http://" + dns
method = input('GET/POST/DELETE: ')

if method.lower() == 'get':
    tasks.get(url)

elif method.lower() == 'post':
    str_body = input('Body: ')
    json_body = json.loads(str_body)
    endpoint = url.split('/')[3]
    tasks.post(url, json_body, end=endpoint)

elif method.lower() == 'delete':
    id_ = input('id: ')
    tasks.delete(url, id_)

else:
    create_log('Closing API')
