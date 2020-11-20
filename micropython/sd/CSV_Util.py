'''
Utility to take a sensor record and log to a CSV file
Works for periodic appending of new data
Author: Howard Webb
Date: 12/14/2019

'''

import os, sys
import pyb
from utime import sleep

env_header = ['type', 'source', 'timestamp', 'subject', 'attribute', 'value', 'units', 'status', 'status_qualifier', 'comment']
file_name = "/sd/data/Data.csv"

class CSV_Util(object):
    
    def __init__(self, file=file_name, header=env_header):
        self._file_name = file
        self._file = None
        print("File", self._file_name)
        try:
            os.stat(self._file_name)
            self._file = self.get_file()
        except:
            # If new append then need header
            self.get_file()
            self.save(header)
            print("Header written")

    def save(self, rec):
       #print(self._file_name)
       self._file.write(', '.join(map(str, rec))+'\n')

    def close(self):
        print("Close file")
        self._file.close()
       
    def check_sd(self):
     
        try:
            os.listdir('/sd')
            print("/sd Mounted")
        except:
            print("SD not found")
            try:
                if pyb.SDCard().present():
                    os.mount(pyb.SDCard(), '/sd')
                    sys.path[1:1] = ['/sd', '/sd/lib']
                    sleep(1)
            except:
               print("Give up on SD")
               return False
        print("SD Mounted")    
        return True        
       
    def get_file(self):
        print("In Get File")
        f = None
        try:
            #print("Found", os.listdir('/sd/data'))
            #print("File", self._file_name)
            f = open(self._file_name, 'a')
            print("Opened", self._file_name)
            return f
            
        except Exception as e:
            print("Failure opening file", self._file_name, e)
            self.check_sd()
            f = open(self._file_name, self._mode)
            return f
        return f
        
      
def test2():
    env_header = ['type', 'source', 'timestamp', 'subject', 'attribute', 'value', 'units', 'status', 'status_qualifier', 'comment']
    rec = ['EnvObsv', '123', '2020-11-03T10:00:00', 'Water', 'Temp', 22, 'C', 'Complete', 'Success', '']
    file_name = "/sd/data/Data.csv"
    
    util = CSV_Util(file_name, env_header)
    print("Save:", file_name)
    util.save(rec)
    print("Done")

#test2()

