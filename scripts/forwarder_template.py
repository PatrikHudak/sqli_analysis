# -*- coding: utf-8 -*-

from __future__ import print_function

import json

import arrow
import requests

# Loads configuration file into dictionary
with open('config.json') as fr:
	global config
	config = json.loads(fr.read())

print('[{0}] Starting alert forwarder...'.format(arrow.utcnow()))

####
# Implement alert delivery + filtering here.
####

payload = {
    'src_ip': '', # Source IP number
    'src_port': '', # Source port number
    'dest_ip': '', # Destination IP address
    'dest_port': '', # Destination port number
    'timestamp': '', # Timestamp of received alert
    'detection': '', # Detection mechanism
    'meta': {
		# Meta information about alert (description etc.)
    }
}

# Sending alert to API
try:
    r = requests.post(config['forwarder']['url'], json=payload)
    if r.status_code != 200:
        raise AssertionError('HTTP response status is {0}'.format(r.status_code))
except (requests.exceptions.ConnectionError, AssertionError) as e:
    print('Alert cannot be delivered. Reason: "{0}"'.format(str(e)))
