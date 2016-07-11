# -*- coding: utf-8 -*-
# A template for new analysis module creation

class Module(object):
	__NAME__ = '' # Your module name

	def __init__(self, env, pcap_path, config):
		self.env = env # Alert dictionary as delivered by alert forwarder
		self.pcap_path = pcap_path # Path to the PCAP file
		self.config = config # config.json provided as a dictionary

	def bootstrap(self):
		###
		# Do testing here
		###

		return {} # Results as a dict
