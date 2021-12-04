from datetime import datetime

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def create_log(text, type=None):
    date = bcolors.HEADER + datetime.now().strftime('%d/%m/%Y %H:%M:%S') + bcolors.ENDC
    message = text
    if type == 'fail':
        message = bcolors.FAIL + text + bcolors.ENDC
    elif type == 'success':
        message = bcolors.OKGREEN + text + bcolors.ENDC
    elif type == 'warning':
        message = bcolors.WARNING + text + bcolors.ENDC
    
    string = "[{0}]: {1}".format(date, message)
    print(string)
    with open(r'./' + 'log.txt', 'a+') as f:
        f.seek(0)
        data = f.read(100)
        if len(data) > 0 :
            f.write("\n")
        f.write("[{0}]: {1}".format(datetime.now().strftime('%d/%m/%Y %H:%M:%S'), text))