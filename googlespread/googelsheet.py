#!/usr/bin/python
# Google spreadsheet API connect to google docs to get data
# from sheet control GPIO
#
# Design by: Nguyen Van Nguyen
# Edit date: 25/6/2018
# Update to python 2.7
# Update function read and write
# Project AGV control of Injection workshop

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from time import sleep


# Init connect raspberry pi to google sheet
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('nguyentrang-eae15422083e.json',scope)
gc = gspread.authorize(credentials)
sheet = gc.open('Test').sheet1
#-------------------------------

while True:
	result = sheet.get_all_records()
	result_dic = result[0]

	print(result)

	sleep(3)
#result = sheet.cell(13,3).value
#sheet.update_cell(13,3,'Nguyễn Văn Nguyện')
#pp.pprint(result)