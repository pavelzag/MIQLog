#!/usr/bin/env python

import random
import string
from tailer import SSHTailer
from termcolor import colored
from time import sleep
username = 'root'
password = ''
random_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(4))


def get_log(server_parameter, log_level='INFO', path='NONE', log_type='None'):
    logfile = open(log_type + "__" + 'log' + "__" + random_string + '.txt', 'w')
    tailer = SSHTailer(server_parameter, path, verbose=True)
    try:
        while 1:
            for line in tailer.tail():
                if log_level == 'ALL':
                    print(line)
                elif 'INFO' in line and 'INFO' in log_level:
                    print (colored(line, 'green'))
                elif 'ERROR' in line and 'ERROR' in log_level:
                    print (colored(line, 'red'))
                logfile.write("%s\n" % line)
            sleep(0.2)
    except KeyboardInterrupt:
        tailer.disconnect()


def log_typer(log_type_abbr):
    if log_type_abbr == 'evm':
        print('The log type that was selected is: ' + log_type_abbr)
        return log_type_abbr
    elif log_type_abbr == 'aut':
        print('The log type that was selected is: \'automation.log\'')
        return 'automation'
    elif log_type_abbr == 'pol':
        print('The log type that was selected is: \'policy.log\'')
        return 'policy'
    elif log_type_abbr == 'api':
        print('The log type that was selected is: \'api.log\'')
        return log_type_abbr
    elif log_type_abbr == 'prod':
        print('The log type that was selected is: \'production.log\'')
        return 'production'
    else:
        print('The log type that was selected is: \'evm.log\'')
        return 'evm'


if __name__ == "__main__":
    server_address = str(raw_input('Enter your CFME address: '))
    log_level = str(raw_input('Select log level (all, info, error): ')).upper()
    log_type_abbr = str(raw_input('Select log type (evm = \'evm\', '
                             'aut = \'automation\', pol = \'policy\', '
                             'api = \'api\', prod = \'production\'): '))
    if not log_level:
        log_level = 'ALL'
    log_type = log_typer(log_type_abbr)
    server_call = username + '@' + server_address
    path = '/var/www/miq/vmdb/log/' + log_type + '.log'
    get_log(server_call, log_level=log_level, path=path, log_type=log_type)
