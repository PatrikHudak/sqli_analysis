# -*- coding: utf-8 -*-
# Forwards Snort alerts to the analysis engine (through API)

from __future__ import print_function

import json
import os

import arrow
import requests
from idstools import unified2, maps

# Loads configuration file into dictionary
with open('config.json') as fr:
	global config
	config = json.loads(fr.read())

sigmap = None
if (os.access(config['forwarder']['sid-map'], os.F_OK & os.R_OK) and
    os.access(config['forwarder']['gid-map'], os.F_OK & os.R_OK)):

    # Loads signatures and generators maps
    sigmap = maps.SignatureMap()
    sigmap.load_signature_map(open(config['forwarder']['sid-map']))
    sigmap.load_generator_map(open(config['forwarder']['gid-map']))

def format_alert_data(event):
	# WARNING/TODO: This needs to be changed!!
	# This if-else is added only to provide correct client/server identification
	# IDS might fire alert both ways, however analysis engine expects only
	# 'HTTP request' alert.
	#
    # Expecting services to have port < 10000
    if event['dport-icode'] < 10000:
        dst = (event['destination-ip'], event['dport-icode'])
        src = (event['source-ip'], event['sport-itype'])
    else:
        src = (event['destination-ip'], event['dport-icode'])
        dst = (event['source-ip'], event['sport-itype'])

    # Create analysis request data
    payload = {
        'src_ip': src[0],
        'src_port': src[1],
        'dest_ip': dst[0],
        'dest_port': dst[1],
        'timestamp': event['event-second'],
        'detection': 'snort',
        'meta': {
            'gid': event['generator-id'],
            'sid': event['signature-id'],
            'rev': event['signature-revision'],
            'cid': event['classification-id']
        }
    }

    if sigmap:
        payload['meta'].update(map_sid(event) or {})

    return payload

def is_correct_signature(alert):
    ''' Filter signatures by correct SID '''
    if event['protocol'] != 6:
        # 0x06 == TCP
        return False

    # Checks if SID is in list of SQLi signatures
    return (int(event['signature-id']) in config['forwarder']['signatures'])

def map_sid(alert):
	''' Map SID and GID to textual description '''
	meta = sigmap.get(alert['generator-id'], alert['signature-id'])
	if not meta:
		return None

	for ref in (meta['ref'] or []):
	    if ref.startswith('http'):
	        meta['ref'] = ref
	        break
	else:
	    meta['ref'] = None

	return {
		'classification': meta['classification'],
		'description': meta['msg'],
		'reference': meta['ref']
	}

print('[{0}] Starting alert forwarder...'.format(arrow.utcnow()))

# Continuous reading from Snort log directory
reader = unified2.SpoolEventReader(	config['forwarder']['logs_dir'],
									config['forwarder']['logs_prefix'],
									follow=True,
									bookmark=True)

for event in reader:
    if not is_correct_signature(event):
        # Event does not match SQLi signatures criteria; ignoring
        continue

    payload = format_alert_data(event)

    # Send alert to API
    try:
        r = requests.post(config['forwarder']['url'], json=payload)
        if r.status_code != 200:
            raise AssertionError('HTTP response status is {0}'.format(r.status_code))
    except (requests.exceptions.ConnectionError, AssertionError) as e:
        print('Alert cannot be delivered. Reason: "{0}"'.format(str(e)))
