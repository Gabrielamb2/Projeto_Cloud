import datetime
from datetime import datetime
import json
from tasks import get,post,delete



dns = input('Insira o DNS do LoadBalancer: ')
url = "http://" + dns
metodo = input("Selecione o método (GET, POST, DELETE): ")

if metodo == 'GET':
    get(url)

elif metodo == 'POST':
    str_body = input('Body: ')
    json_body = json.loads(str_body)
    endpoint = url.split('/')[3]
    post(url, json_body, end=endpoint)


elif metodo == 'DELETE':

    id_ = input('id: ')
    delete(url, id_)

else:
    print("Fechando API")
    print("\n")
    
