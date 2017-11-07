#!/usr/bin/env python

import random
import string
from tailer import SSHTailer
from termcolor import colored
from time import sleep
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import email.mime.application
import configuration
import os
from os import path

username = configuration.get_miq_config('user')
password = configuration.get_miq_config('pass')
random_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(4))
smtp_user = configuration.get_smtp_config('user')
smtp_passwd = configuration.get_smtp_config('pass')


def get_log(server_parameter, server_address, password, log_level='INFO', log_path='NONE', log_type='None', send_to = 'None'):
    tailer = SSHTailer(server_parameter, log_path, password, verbose=True)
    logs_directory = 'logs'
    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)
    log_file_path = path.join(logs_directory, '{}_{}_{}{}'.format(log_type, 'log', random_string, '.txt'))
    logfile = open(log_file_path, 'w')
    print('{} {}'.format('Printing local log at:', logfile.name))
    try:
        while 1:
            for line in tailer.tail():
                if log_level == 'ALL':
                    if 'INFO' in line:
                        print (colored(line, 'green'))
                    elif 'ERROR' or 'FATAL' in line:
                        print (colored(line, 'red'))
                    elif 'WARN' in line:
                        print (colored(line, 'yellow'))
                elif 'INFO' in line and 'INFO' in log_level:
                    print (colored(line, 'green'))
                elif 'ERROR' in line and 'ERROR' in log_level:
                    print (colored(line, 'red'))
                logfile.write("%s\n" % line)
            sleep(0.2)
    except KeyboardInterrupt:
        tailer.disconnect()
        logfile.close()
        if not 'none' in send_to:
            send_mail(send_to=send_to, subject='{}{} {}'.format(log_type, '.log incoming for', server_address), file_name=logfile.name)
        else:
            print('skipping e-mail')


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


def send_mail(send_to, subject, file_name=None, smtp_user=smtp_user, smtp_passwd=smtp_passwd,
              server="smtp.gmail.com"):
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    body = email.mime.Text.MIMEText("""Your requested log is attached here""")
    msg.attach(body)

    fp = open(file_name, 'rb')
    att = email.mime.application.MIMEApplication(fp.read(), _subtype="txt")
    fp.close()
    att.add_header('Content-Disposition', 'attachment', filename=file_name)
    msg.attach(att)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(smtp_user, smtp_passwd)
    s.sendmail(smtp_user, send_to, msg.as_string())
    print('{} {}'.format('sending mail to:', send_to))
    s.quit()


if __name__ == "__main__":
    server_address = str(raw_input('Enter your CFME address: '))
    log_level = str(raw_input('Select log level (all, info, error): ')).upper()
    log_type_abbr = str(raw_input('Select log type (evm = \'evm\', '
                             'aut = \'automation\', pol = \'policy\', '
                             'api = \'api\', prod = \'production\'): '))
    send_to_address = str(raw_input('Where would you like to send the mail: (Enter e-mail address or none to skip) ')).lower()
    if not send_to_address:
        send_to_address = 'none'
    if not log_level:
        log_level = 'ALL'
    log_type = log_typer(log_type_abbr)
    server_call = '{}{}{}'.format(username, '@', server_address)
    log_path = path.join('/var/www/miq/vmdb/log/', log_type + '.log')
    get_log(server_call, server_address, password, log_level=log_level, log_path=log_path, log_type=log_type, send_to=send_to_address)
