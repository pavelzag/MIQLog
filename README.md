# MIQLog
Gain easy access to Manage IQ Logs

This is a simple script that allows simple access to different ManageIQ logs.

# Setting up:
Before running change to your machines' usernames and the passwords if required.

# Running:
The prompt will ask you the following:

Enter your CFME address: <Your MIQ Appliance>

Select log level (all, info, error): <all is selected by default>

Select log (evm = 'evm', aut = 'automation', pol = 'policy', api = 'api', prod = 'production'): <evm.log is selected by default>


The script uses slightly modified fork of this app:
https://github.com/praekelt/python-sshtail
