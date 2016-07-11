# -*- coding: utf-8 -*-
# Analysis engine implementation

import os
import json
import time
from urlparse import urljoin

import arrow
import celery
import requests
import rethinkdb as r
from requests.auth import HTTPDigestAuth
from requests.packages.urllib3.exceptions import 	(InsecureRequestWarning,
													SNIMissingWarning,
													InsecurePlatformWarning)


from modules import __all__ as modules_list

requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(SNIMissingWarning)

# Loads configuration file into dictionary
with open('config.json') as fr:
	global config
	config = json.loads(fr.read())

celery_app = celery.Celery('engine')
celery_app.config_from_object(config['celery'])

def get_modules():
	""" Gets list of postprocessing modules """
	modules = __import__('modules', fromlist=modules_list)
	return [getattr(getattr(modules, mod), 'Module') for mod in modules_list]

def request_pcap(opts):
	""" Retrieves filtered PCAP from Moloch """
	if not os.access(config['pcap_directory'], os.W_OK):
		raise IOError('PCAP folder is not writable')

	# Create Moloch expression query
	moloch_expression =  'port.dst == {dest_port}'
	moloch_expression += '&& protocols == http'
	moloch_expression += '&& ip.src == {src_ip}'
	moloch_expression += '&& ip.dst == {dest_ip}'
	# Add values to template
	moloch_expression = moloch_expression.format(**opts)

	# Generate filename for PCAP
	pcap_file = '{ip}.{stime}.pcap'.format(ip=opts.get('src_ip').replace('.', '-'), stime=opts.get('timestamp'))

	moloch_api_url = urljoin(config['moloch']['viewer'], 'sessions.pcap')
	moloch_api_auth = HTTPDigestAuth(config['moloch']['username'], config['moloch']['password'])

	# Create HTTP request data
	payload = {
		'expression': moloch_expression,
		'startTime': opts.get('timestamp'),
		'stopTime': arrow.utcnow().timestamp # currect UTC time in as UNIX timestamp
	}

	# Make a HTTP request and save retrieved data to file
	r = requests.get(moloch_api_url, auth=moloch_api_auth, params=payload, stream=True, verify=False, timeout=5)
	with open(os.path.join(config['pcap_directory'], pcap_file), 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024):
			if chunk: f.write(chunk)

	return pcap_file

@celery_app.task(bind=True)
def analyze(self, analysis_data, pcap_path=None):
	""" Analyses alert """
	error = None
	start_time = time.time()

	# Create RethinkDB connection
	rdb = r.connect(host=config['rethinkdb']['host'],
					port=config['rethinkdb']['port'],
					db=config['rethinkdb']['db'])

	analysis = {}

	# NOTE: r.now() cannot be used, because the result of the function is evaluated
	# when query is run. This is OK for the first update function. However, the second
	# run will replace this time, which is not intended.
	analysis['job_start'] = r.iso8601(str(arrow.utcnow()))
	analysis['job_status'] = r.literal({
		'state': 'PROGRESS'
	})

	# Update the database entry for status update
	r.table('analysis').get(self.request.id).update(analysis).run(rdb)

	# pcap_path is not None when provided using Web form
	if not pcap_path:
		try:
			analysis['pcap_file'] = request_pcap(analysis_data)
			pcap_path = os.path.join(config['pcap_directory'], analysis['pcap_file'])
		except (IOError, requests.ConnectionError) as e:
			error = str(e)
			pcap_path = None

	# Check PCAP file permissions
	if pcap_path and not os.access(pcap_path, os.F_OK & os.R_OK):
		error = 'PCAP file can not be accessed'

	# Check if retrieved PCAP is non-empty
	if pcap_path and os.stat(pcap_path).st_size == 0:
		error = 'PCAP file does not contain any data'

	try:
		modules = get_modules()
	except (ImportError, ) as e:
		error = 'Modules can not be imported. Reason: "{0}"'.format(str(e))

	if error:
		analysis['job_status'] = r.literal({
			'state': 'ERROR',
			'error': error
		})

		r.table('analysis').get(self.request.id).update(analysis).run(rdb)
		rdb.close()
		return error # end the Celery task

	# Everything is ready = starting the analysis
	analysis['results'] = {}

	for mod in modules:
		module_name = mod.__NAME__
		try:
			analysis['results'][module_name] = mod(analysis_data, pcap_path, config).bootstrap()
		except (Exception, ) as e:
			analysis['results'][module_name] = {'error': str(e)}

	analysis['exec_time'] = round(time.time() - start_time, 2)
	analysis['job_status'] = r.literal({
		'state': 'SUCCESS'
	})

	r.table('analysis').get(self.request.id).update(analysis).run(rdb)
	rdb.close()
