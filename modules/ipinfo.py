# -*- coding: utf-8 -*-
# Analysis module for source IP address info retrieval
# Gathered details: ASN, CIDR, Country, ISP,

import urllib

import ipwhois
import pycountry

class Module(object):
	__NAME__ = 'ipinfo'

	def __init__(self, env, pcap_path, config):
		self.ip = env['src_ip']
		self.ip_info = {}

	def bootstrap(self):
		try:
			self.ip_info = self.whois()
		except (Exception, ) as e:
			return {'error': str(e)}

		# check is IP is Tor exit node only if is public and there were no errors
		self.ip_info['is_tor'] = self.is_tor()

		return self.ip_info

	def find_abuse(self, objs):
		for o in objs.values():
			if o['roles'] and 'abuse' in o['roles'] and o['contact']['email']:
				abuse_email = o['contact']['email'][0].get('value', None)
				if abuse_email: return abuse_email
		return None

	def is_tor(self):
		exit_nodes = urllib.urlopen('http://torstatus.blutmagie.de/ip_list_exit.php/Tor_ip_list_EXIT.csv')
		for ip in exit_nodes.readlines():
			if self.ip == ip.strip(): return True
		return False

	def whois(self):
		whois_info = {}

		info = ipwhois.IPWhois(self.ip, timeout=5)
		info = info.lookup_rdap(depth=1)

		whois_info['asn'] = info['asn']
		if whois_info['asn'] == 'NA':
			whois_info['asn'] = None

		whois_info['cidr'] = info['network'].get('cidr', None)
		whois_info['country'] = info['network'].get('country', None)
		if whois_info['country']:
			# convert to readable format
			try:
				whois_info['country'] = pycountry.countries.get(alpha2=whois_info['country'])
				whois_info['country'] = whois_info['country'].name
			except(KeyError, ):
				whois_info['country'] = None

		whois_info['isp'] = None
		if type(info['network']['remarks']) == list and info['network']['remarks']:
			whois_info['isp'] = info['network']['remarks'][0].get('description', None)

		whois_info['abuse'] = self.find_abuse(info['objects'])
		return whois_info
