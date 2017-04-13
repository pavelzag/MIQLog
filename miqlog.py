#!/usr/bin/env python

from tailer import SSHTailer
from time import sleep
username = 'root'
password = ''


def get_log(server_parameter, log_level='INFO', path='NONE'):
    tailer = SSHTailer(server_parameter, path, verbose=True)
    try:
        while 1:
            for line in tailer.tail():
                if log_level == 'ALL':
                    print line
                elif 'INFO' in line and 'INFO' in log_level:
                    print line
                elif 'ERROR' in line and 'ERROR' in log_level:
                    print line
            sleep(0.2)
    except:
        tailer.disconnect()


def log_typer(log_type_abbr):
    if log_type_abbr == 'evm':
        return log_type_abbr
    elif log_type_abbr == 'aut':
        return 'automation'
    elif log_type_abbr == 'pol':
        return 'policy'
    elif log_type_abbr == 'api':
        return log_type_abbr
    elif log_type_abbr == 'prod':
        return 'production'
    else:
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
    get_log(server_call, log_level=log_level, path=path)
