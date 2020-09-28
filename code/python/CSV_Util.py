'''
Utility to take a sensor record and log to a CSV file
Author: Howard Webb
Date: 12/14/2019

sudo pip3 install get-mac
'''

import csv
from datetime import datetime
import math
import os


DIR = '/home/pi/data/'
header = ['type', 'source', 'timestamp', 'subject', 'attribute', 'value', 'units', 'status', 'status_qualifier', 'comment']


class CSV_Util(object):
    
    def __init__(self, logger=None):
        self._file_name = "Data.csv"
        if not os.path.isfile(DIR + self._file_name):
            self.save(header)
        
    def save(self, rec):
       with open(DIR + self._file_name, 'a+', newline='') as f: 
           wr = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
           wr.writerow(rec)
      
    def get_list(self):
       with open( DIR + self._file_name, 'r') as f:
           rr = csv.reader(f, delimiter=',',quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
           doc = list(rr)
           #print(doc)
           return doc


def test():
    print("CSV_Util Test")
    util = CSV_Util()
    from TestRecords import recs
    for rec in recs:
        print(rec)
        util.save(rec)
    print("Done")
    util.get_list()
    
def test2():
    util = CSV_Util()
    util.get_list()
    
if __name__=="__main__":
    test()

