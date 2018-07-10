#!/usr/bin/python
# Serial connect
#
# Design by: Nguyen Van Nguyen
# Edit date: 25/6/2018
# Update to python 2.7
# Update function read and write
# Project AGV control of Injection workshop

# Import library
import serial


# Init class serial

class Serial(object):
    cport = ''
    cbaudrate = 0
    ctimeout = 0
    isConnected = False

    def __init__(self,port,baudrate,timeout=1):
        self.cport = port
        self.cbaudrate = baudrate
        self.ctimeout = timeout
        self.isConnected = False

    def Open(self):
        try:
            cser = serial.Serial(self.cport,self.cbaudrate,timeout=self.ctimeout)
            self.isConnected = True
            return cser
        except:
            print 'Connect Error'
            self.isConnected = False
            return None

    def Close(self,ser):
        if ser != None:
            ser.close()

    def Read_Data(self):
        ser = self.Open()
        if ser != None:
            data_resp = ser.readline()
            self.Close(ser)
            return data_resp
        return None

    def Write_Data(self,data):
        ser = self.Open()
        if ser != None:
            ser.write(data)
            self.Close(ser)
            return True
        return False