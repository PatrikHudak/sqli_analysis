# -*- coding: utf-8 -*-
# This module implements discovery of underlying technologies on website
# Fingerprint services used: Wappalyzer

import collections
import random

from requests.structures import CaseInsensitiveDict
import Wappalyzer

from . import utils

WappPage = collections.namedtuple('WappPage', 'url text headers')

class Module(object):
	__NAME__ = 'websiteinfo'

	def __init__(self, env, pcap_path, config):
		self.ip = env['dest_ip']
		self.http_flow = utils.extract_http_from_pcap(pcap_path, responses_only=True)

	def bootstrap(self):
		filtered = [resp for resp in self.http_flow if (u'200' in resp['status']
														and u'text/html' in resp['content_type'].lower()
														and resp['payload'])]

		if len(self.http_flow) == 0 or len(filtered) == 0:
			return {'error': 'no HTML responses in PCAP'}

		sample = random.choice(filtered)
		sample = WappPage(
			url='',
			text=sample['payload'],
			headers=self.headers_to_dict(sample['headers'])
		)

		wappalyzer = Wappalyzer.Wappalyzer.latest()
		webpage = Wappalyzer.WebPage.new_from_response(sample)

		return {'technologies': list(wappalyzer.analyze(webpage))}

	def headers_to_dict(self, headers):
		entries = headers.replace('\r', '').split('\n')
		headers = CaseInsensitiveDict()
		for h in entries:
			h = h.split(': ')
			headers[h[0].encode('utf-8')] = h[1].encode('utf-8')
		return headers
