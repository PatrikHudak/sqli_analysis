# -*- coding: utf-8 -*-

from __future__ import division

from collections import Counter

import utils

class Module(object):
	__NAME__ = 'statistics'
	
	def __init__(self, env, pcap_path, config):
		self.http_traffic = utils.extract_http_from_pcap(pcap_path)

	def bootstrap(self):
		endpoints = []
		mime = []
		user_agents = []

		# Extract fields of interest
		for p in self.http_traffic:
			if p['type'] == 'request':
				endpoints.append(p['path'].strip().lower())
				user_agents.append(str(p['ua']).strip())
			elif p['type'] == 'response' and p.get('content_type'):
				mime.append(p['content_type'].split(';')[0].strip().lower())

		# Compute ratio of values (Top 5 values)
		endpoints = [(e[0], round(e[1] / len(endpoints), 2)) for e in Counter(endpoints).most_common(5)]
		mime = [(e[0], round(e[1] / len(mime), 2)) for e in Counter(mime).most_common(5)]
		user_agents = [(e[0], round(e[1] / len(user_agents), 2)) for e in Counter(user_agents).most_common(5)]

		return {
			'endpoints': endpoints,
			'mime': mime,
			'user_agents': user_agents
		}
