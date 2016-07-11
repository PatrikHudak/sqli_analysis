# -*- coding: utf-8 -*-
# Analysis module implements attacker's connections visualization using Moloch API

from urlparse import urljoin

import requests
from requests.auth import HTTPDigestAuth

class Module(object):
	__NAME__ = 'connections'

	def __init__(self, env, pcap_path, config):
		self.src_ip = env['src_ip']
		self.dst_ip = env['dest_ip']
		self.config = config

	def bootstrap(self):
		url = urljoin(self.config['moloch']['viewer'], 'connections.json')
		auth = HTTPDigestAuth(self.config['moloch']['username'], self.config['moloch']['password'])

		payload = {
			'date': 168,
			'expression': 'ip.src == {0}'.format(self.src_ip),
		}

		connections = requests.get(url, auth=auth, params=payload, stream=True, verify=False, timeout=5).json()

		# Convert to `visjs` format	
		nodes = []
		for node in connections['nodes']:
			if node['id'] == self.src_ip:
				nodes.append({
					'id': node['pos'],
					'label': '{0}\n\nSessions: {1}\nBytes: {2}'.format(node['id'], node['sessions'], node['by']),
					'shape': 'box',
					'color': '#d9534f'
				})
			elif node['id'] == self.dst_ip:
				nodes.append({
					'id': node['pos'],
					'label': '{0}\n\nSessions: {1}\nBytes: {2}'.format(node['id'], node['sessions'], node['by']),
					'shape': 'box',
					'color': '#5cb85c'
				})
			else:
				nodes.append({
					'id': node['pos'],
					'label': node['id']
				})

		edges = []
		for edge in connections['links']:
			edges.append({
				'from': edge['source'],
				'to': edge['target'],
				'label': '{0} bytes'.format(edge['by'])
			})

		if len(edges) == 0 or len(nodes) == 0:
			return {'error': 'No connections found'}
		return {'nodes': nodes, 'edges': edges}
