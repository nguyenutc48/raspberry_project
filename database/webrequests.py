#!/usr/bin/python
# Main Processing
#
# Design by: Nguyen Van Nguyen
# Edit date: 25/6/2018
# Update to python 2.7
# Update function read and write
# Project AGV control of Injection workshop

# Include library
import requests

class webrequest(object):

	ip_address = '192.168.0.115'
	url_true = 'http://'+ip_address+'/api/line/true'
	url_false = 'http://'+ip_address+'/api/line/false'

	def __init__(self):
		try:
			r = requests.get(self.url_false,timeout=None)
			if r.status_code == 200:
				print('Connect success!')
		except:
			print('Connect false!')

	def request_agv(self):
		r = requests.get(self.url_true,timeout=2)
		if r.status_code == 200:
			print('Request done!')
			return True
		else:
			return False
