# -*- coding: utf-8 -*-

#disable scapy warnings
import logging
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)


#disable requests SSL warnings
import requests
from requests.packages.urllib3.exceptions import 	(InsecureRequestWarning,
													SNIMissingWarning,
													InsecurePlatformWarning)

requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(SNIMissingWarning)

# this list include all postprocessing modules
# that will be used during the analysis
__all__ = [
    'connections',
    'ipinfo',
    'websiteinfo',
	'canary',
	'statistics'
]
