#!/usr/bin/python
# Serial connect
#
# Design by: Nguyen Van Nguyen
# Edit date: 25/6/2018
# Update to python 2.7
# Update function read and write
# Project AGV control of Injection workshop

# Import library
from serial_connect import Serial
from log.logfile import LogFile

# Define variable of communication frame
HEADER_REQUEST = '\x05'
HEADER_RESPONSE_OK = '\x06'
HEADER_RESPONSE_ERROR = '\x15'
TAIL_REQUEST = '\x04'
TAIL_RESPONSE = '\x03'
STATION_NUMBER = '00'
COMMAND_READ = 'R'
COMMAND_WRITE = 'W'
COMMAND_TYPE = 'SB'
DEVICE_LENGTH = '08'
NUMBER_OF_DATA_REQUEST = '01'
NUMBER_OF_DATA_RESPONSE = '02'
DATA_REQUEST_WRITE = ''
DATA_RESPONSE_READ = ''
DATA_RESPONSE_ERROR = ''
DEVICE_WRITE_ADDRESS = '00000'
DEVICE_READ_ADDRESS = '00000'
DEVICE_WRITE_BLOCK = ''
DEVICE_READ_BLOCK = ''
DEVICE_WRITE_BLOCK_INDEX = 5
DEVICE_READ_BLOCK_INDEX = 5
DATA_REQUEST_WRITE_INDEX = 7

FR_READ_REQUEST = [HEADER_REQUEST,STATION_NUMBER,COMMAND_READ,COMMAND_TYPE,DEVICE_LENGTH,
                   DEVICE_READ_BLOCK,
                   NUMBER_OF_DATA_REQUEST,TAIL_REQUEST]
FR_WRITE_REQUEST = [HEADER_REQUEST,STATION_NUMBER,COMMAND_WRITE,COMMAND_TYPE,DEVICE_LENGTH,
                    DEVICE_WRITE_BLOCK,NUMBER_OF_DATA_REQUEST,
                    DATA_REQUEST_WRITE,TAIL_REQUEST]

# Init class of project
class Cnet(object):

    plc_ser  = None
    ser = None

    def __init__(self,port,baudrate,timeout):
        self.ser = Serial(port,baudrate,timeout)
        self.plc_ser = self.ser.Open()
        #print(self.plc_ser)

    def PLC_Read(self,address):
        val_return = -1
        if address.find('.') == -1:
            val_return = self.Send_Command_Read(address)
        else:
            addr_reg_temp,addr_bit_temp = address.split('.')
            val_resp = self.Send_Command_Read(addr_reg_temp)
            bit_index = self.Address2BitIndex(addr_bit_temp)
            if val_resp == None:
                return -1
            data_calculator = val_resp & (1 << bit_index)
            val_return = data_calculator >> bit_index
        return val_return

    def PLC_Write(self,address,value):
        val_return = -1
        if address.find('.') == -1:
            val_return = self.Send_Command_Write(address,value)
        else:
            addr_reg_temp, addr_bit_temp = address.split('.')
            if len(addr_bit_temp) != 1:
                val_return = -1
            else:
                val_resp = self.Send_Command_Read(addr_reg_temp)
                if val_resp == None:
                    return -1
                bit_index = self.Address2BitIndex(addr_bit_temp)
                if bit_index > 15:
                    val_return = -1
                else:
                    if value == 1:
                        data_calculator = val_resp | (1 << bit_index)
                        val_return = self.Send_Command_Write(address, data_calculator)
                    elif value == 0:
                        data_calculator = val_resp & ~(1 << bit_index)
                        val_return = self.Send_Command_Write(address, data_calculator)
                    else:
                        val_return = -1
        return val_return

    def Send_Command_Read(self,address_reg):
        addr_reg = self.Address2DeviceBlockReg(address_reg)
        FR_READ_REQUEST[DEVICE_READ_BLOCK_INDEX] = addr_reg
        command = self.Array2String(FR_READ_REQUEST)
        command_send = command.encode()
        self.ser.Write_Data(command_send)
        data_response = self.ser.Read_Data()

        # Check error if you want
        if data_response != None:
            return self.Response_Value(data_response)
        else:
            return None


    def Send_Command_Write(self,address,data):
        block_address = self.Address2DeviceBlockReg(address)
        FR_WRITE_REQUEST[DEVICE_WRITE_BLOCK_INDEX] = block_address
        FR_WRITE_REQUEST[DATA_REQUEST_WRITE_INDEX] = self.int_to_bcd(data)
        command = self.Array2String(FR_WRITE_REQUEST)
        command_send = command.encode();
        self.ser.Write_Data(command_send)
        data_response = self.ser.Read_Data()
        err = self.Check_Error(data_response)
        if err == True:
            return -1
        else:
            return 0

    def Address2DeviceBlockReg(self,address):
        str_device_label = address[0]
        str_register_address = address[1:len(address)]
        array_address = self.Address_To_Command(str_register_address)
        str_address = ''
        for i in array_address:
            str_address += i
        device_register_address = str_address
        device_block = '%' + str_device_label + 'W' + device_register_address
        return device_block

    def Address2DeviceBlockBitReg(self,address):
        str_device_label = address[0]
        str_register_address = address[1:len(address) - 1]
        array_address = self.Address_To_Command(str_register_address)
        str_address = ''
        for i in array_address:
            str_address += i
        device_register_address = str_address
        device_block = '%' + str_device_label + 'W' + device_register_address
        return device_block

    def Address_To_Command(self,raw_address):
        str_format_address = ['0','0','0','0','0']
        len_raw_address = len(raw_address)
        count = 4
        for x in range(len_raw_address):
            str_format_address[count] = raw_address[(len_raw_address-1)-x]
            count-=1
            if count == -1:
                return str_format_address
        return str_format_address

    def Array2String(self,array):
        str_temp = ''
        for x in array:
            str_temp+=x
        return str_temp

    def Response_Value(self,raw_data):
        data = raw_data.decode('utf-8')
        data_change = data[1:len(data)-1]
        if data_change.find(NUMBER_OF_DATA_RESPONSE) == -1:
            return None
        else:
            temp,val = data_change.split(NUMBER_OF_DATA_RESPONSE)
        return int(val,16)

    def Address2BitIndex(self,address):
        str_bit_address = address[len(address) - 1]
        ibit_address = int(str_bit_address, 16)
        return ibit_address

    def int_to_bcd(sefl,val):
        temp = '%x' % val
        temp_len = len(temp)
        str_temp = ['0','0','0','0']
        for i in range(4):
            if (temp_len-1)-i>=0:
                str_temp[3-i] = temp[(temp_len-1)-i]
            else:
                return sefl.Array2String(str_temp)
        return sefl.Array2String(str_temp)

    def Check_Error(self,data_response):
        if data_response[0] == 21:
            print 'Command send error'
            return True
        else:
            return False
