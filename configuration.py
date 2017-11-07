import yaml


def get_miq_config(parameter_name):
    with open("creds.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    if parameter_name == 'user':
        return cfg['creds']['miq_user']
    if parameter_name == 'pass':
        return cfg['creds']['miq_pass']


def get_smtp_config(parameter_name):
    with open("creds.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    if parameter_name == 'user':
        return cfg['creds']['sftp_user']
    if parameter_name == 'pass':
        return cfg['creds']['sftp_pass']