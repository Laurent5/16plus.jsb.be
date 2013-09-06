'''
    Software configuration. It is an executable Python file and is
    imported for access to the variables.
'''

import os.path

# Identity verification through Mozilla Persona requires the hostname to
# be sent in the checking request.

import platform
if platform.node() == 'lithium':
    hostname = 'localhost:1616'
    DATA_PATH = os.path.expanduser('~') + '/Desktop/16plus.jsb.be/data'
else:
    hostname = '16plus.jsb.be'
    DATA_PATH = os.path.expanduser('~') + '/apps/16plus.jsb.be/data'

    
REGISTRATIONS_PATH = DATA_PATH + '/registrations'
JSON_PATH = DATA_PATH + '/json'
