'''
w  write mode
r  read mode
a  append mode

w+  create file if it doesn't exist and open it in write mode
r+  open an existing file in read+write mode
a+  create file if it doesn't exist and open it in append mode
'''


# Import library
import datetime

class LogFile(object):
    cpath = ''
    cfile_name = ''
    cf = None

    def __init__(self,path,file_name):
        self.cpath = path
        self.cfile_name = file_name
        #full_path = self.cpath+self.cfile_name
        #self.cf = open(full_path,'a+')

    def Add_Log(self,text):
        full_path = self.cpath+self.cfile_name
        f = open(full_path,'a+')
        f.write(text+'\r\n')
        f.close()

    def Add_Log_Current_Date(self,text):
        nowtime = datetime.datetime.now().isoformat()
        a, b = nowtime.split("T")
        strdate = a
        strtime = b
        full_path = self.cpath+self.cfile_name
        f = open(full_path,'a+')
        f.write(strdate+', '+strtime+': '+text+'\r\n')
        f.close()
