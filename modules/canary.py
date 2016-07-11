# -*- coding: utf-8 -*-
# Analysis module implements canary detection in server responses

import rethinkdb as r

import utils

class Module(object):
	__NAME__ = 'canary'

	def __init__(self, env, pcap_path, config):
		self.config = config
		self.http_traffic = utils.extract_http_from_pcap(pcap_path, responses_only=True)
		self._get_canaries()

	def bootstrap(self):
		canary_found = False

		for response in self.http_traffic:
			for canary in self.canaries:
				if response.get('payload') and canary in response['payload']:
					canary_found = canary
					break

		return {'found': canary_found}

	def _get_canaries(self):
		rdb = r.connect(host=self.config['rethinkdb']['host'],
						port=self.config['rethinkdb']['port'],
						db=self.config['rethinkdb']['db'])
		self.canaries = list(r.table('canary').get_field('canary').run(rdb))
		rdb.close()
