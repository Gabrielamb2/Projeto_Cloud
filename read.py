import json

def read_command(file_name, is_json=False):
    path = r'./' + '/'
    with open(path+file_name, 'r') as file:
        if is_json:
            return json.load(file)
        return file.read()