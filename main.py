#!/usr/bin/env python
# Main Processing
#
# Design by: Nguyen Van Nguyen
# Edit date: 25/6/2018
# Update to python 2.7
# Update function read and write
# Project AGV control of Injection workshop

# Import library
from plc.plc_ls_cnet_com import Cnet as plc
from log.logfile import LogFile
from time import sleep
import requests
import os
import json
import pprint
from pyroute2 import IPDB
import socket, struct, fcntl

i_trayinput = 0
ip_address = '107.114.184.180'
url_true = 'http://'+ip_address+'/api/line/true'
url_false = 'http://'+ip_address+'/api/line/false'



def setupIP(ipaddr):
	os.system('sudo ifconfig eth0 down')
	os.system('sudo ifconfig eth0 %s/24 netmask 255.255.255.0'% (ipaddr))
	#os.system('sudo ip addr change dev eth0 %s/24' % (ipaddr))
	os.system('sudo route add default gw 107.117.216.1 eth0')
	os.system('sudo ifconfig eth0 up')

def getIP(macaddr):
	a = open('/home/pi/nguyenproject/ips.json', 'r')
	json_decoded = json.load(a)
	try:
		return json_decoded[macaddr]
	except:
		print 'Khong ton tai'
		return None
def getEthName():
	# Get name of the Ethernet interface
	try:
		for root,dirs,files in os.walk('/sys/class/net'):
			for dir in dirs:
				if dir[:3]=='enx' or dir[:3]=='eth':
					interface=dir
	except:
		interface="None"
	return interface

def getMAC(interface='eth0'):
	# Return the MAC address of the specified interface
	try:
		str = open('/sys/class/net/%s/address' %interface).read()
	except:
		str = "00:00:00:00:00:00"
	return str[0:17]

def request_agv(url):
	try:
		r = requests.get(url, timeout=None)
		if r.status_code == 200:
			print('Connect success!')
			return True
	except requests.exceptions.RequestException as e:
		print('Disconnect to server')
		print(e)
		return False


if __name__ == '__main__':
	ethName=getEthName()
	ethMAC=getMAC(ethName)
	MAC = ethMAC.upper()
	print(MAC)
	ip = getIP(MAC)
	print(ip)
	if ip != None:
		setupIP(ip)
		sleep(10)
		req_memo = 0
		con = plc('/dev/ttyUSB0', 38400, 2)
		while True:
			a = con.PLC_Read('P0012.6')
			b = con.PLC_Read('P0012.5')
			print a
			print b
			if a == 0 and b == 0:
				sleep(5)
				print 'Dang can AGV'
				if a == con.PLC_Read('P0012.6') and b == con.PLC_Read('P0012.5'):
					req_status = request_agv(url_true)
					if req_status == True:
						print('Request AGV Done!')
			else:
				sleep(5)
				print 'Bao khong can AGV'
				req_status = request_agv(url_false)
				if req_status == True:
					print('Eo can AGV nua!')
			sleep(10)
	else:
		print 'Khong cai dat duoc dia chi IP'




