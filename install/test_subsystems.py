# -*- coding: utf-8 -*-

import json
import os
from urlparse import urljoin

import requests
import rethinkdb as r
from requests.auth import HTTPDigestAuth
from requests.packages.urllib3.exceptions import 	(InsecureRequestWarning,
													SNIMissingWarning,
													InsecurePlatformWarning)



requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(SNIMissingWarning)

config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../config.json')

with open(config_file) as fr:
	config = json.loads(fr.read())

def test_rethinkdb():
	rdb = r.connect(	host=config['rethinkdb']['host'],
						port=config['rethinkdb']['port'],
						db=config['rethinkdb']['db'],
						timeout=3)
	rdb.close()

def test_moloch():
	moloch_api_auth = HTTPDigestAuth(config['moloch']['username'], config['moloch']['password'])
	moloch_api_url = urljoin(config['moloch']['viewer'], 'connections.json')
	try:
		req = requests.get(moloch_api_url, auth=moloch_api_auth, verify=False, timeout=5)
		if req.status_code != 200:
			raise AssertionError
	except (requests.ConnectionError, AssertionError):
		raise AssertionError('Error connecting to Moloch on {0}'.format(config['moloch']['viewer']))

def test_api():
	try:
		req = requests.get(config['forwarder']['url'], verify=False, timeout=5)
		if req.status_code != 200:
			raise AssertionError
	except (requests.ConnectionError, AssertionError):
		raise AssertionError('Error connecting to API on {0}'.format(config['forwarder']['url']))

def test_amqp():
	pass

test_rethinkdb()
test_moloch()
test_api()
test_amqp()
