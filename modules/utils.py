# -*- coding: utf-8 -*-

import urlparse
import zlib

import user_agents
from scapy.all import *
from scapy.layers import http

def decompress_payload(data, encoding):
	if not encoding:
		# text/plain
		return data

	if encoding == u'gzip':
		return zlib.decompress(data, 16+zlib.MAX_WBITS)

def extract_http_from_pcap(pcap_path, requests_only=False, responses_only=False):
	http_flow = []
	packets = rdpcap(pcap_path)

	for h in packets:
		if not h.haslayer(http.HTTP):
			# interested only in HTTP packets
			continue

		http_request = h.getlayer(http.HTTPRequest)
		http_response = h.getlayer(http.HTTPResponse)

		network_layer = h.getlayer(IP)
		transport_layer = h.getlayer(TCP)

		fields = {}
		if http_request and not responses_only:
			fields['type'] = 'request'
			fields['method'] = http_request.getfieldval('Method')
			fields['host'] = http_request.getfieldval('Host')
			fields['encoding'] = http_request.getfieldval('Content-Encoding')
			fields['ua'] = http_request.getfieldval('User-Agent')
			fields['cookie'] = http_request.getfieldval('Cookie')
			fields['referer'] = http_request.getfieldval('Referer')
			fields['http_version'] = http_request.getfieldval('Http-Version')

			# url dissect
			path = urlparse.urlparse(http_request.getfieldval('Path'))
			fields['path'] = path.path
			fields['query'] = path.query

			data = h.getlayer(Raw)
			if data:
				fields['payload'] = decompress_payload(data.getfieldval('load'), fields['encoding'])

		if http_response and not requests_only:
			fields['type'] = 'response'
			fields['status'] = http_response.getfieldval('Status-Line')
			fields['server'] = http_response.getfieldval('Server')
			fields['encoding'] = http_response.getfieldval('Content-Encoding')
			fields['content_type'] = http_response.getfieldval('Content-Type')
			fields['headers'] = http_response.getfieldval('Headers')

			data = h.getlayer(Raw)
			if data:
				fields['payload'] = decompress_payload(data.getfieldval('load'), fields['encoding'])

		if fields:
			fields['src_ip'] = network_layer.getfieldval('src')
			fields['dst_ip'] = network_layer.getfieldval('dst')
			fields['src_port'] = transport_layer.getfieldval('sport')
			fields['dst_port'] = transport_layer.getfieldval('dport')
			http_flow.append(fields)

	return http_flow
