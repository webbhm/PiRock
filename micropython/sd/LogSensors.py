'''
Log Sensors to CSV file
Called from /home/pi/scripts/LogSensors.sh - needs to be uncommented for to run
Author: Howard Webb
Date: 9/28/2020
'''

from CSV_Util import CSV_Util
from env import env
from pyb import RTC

env_header = ['type', 'site_id', 'timestamp', 'lat', 'long', 'subject', 'attribute', 'value', 'units', 'status', 'status_qualifier', 'comment']
env_file_name = "/sd/data/Data.csv"


class LogSensors(object):

    def __init__(self, file=env_file_name, header=env_header):
        """Record optional sensor data
        Args:
            lvl: Logging level
        Returns:
            None
        Raises:
            None
        """        
        self._activity_type = "Environment_Observation"
        self._persist = CSV_Util(file, header)
        self.test = False
        self._id = env['id']
        self._lat = "{:1.6f}".format(env['location']['lat'])
        self._long = "{:1.6f}".format(env['location']['long'])
        dt = RTC().datetime()
        self._ts = "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(dt[0], dt[1], dt[2], dt[4], dt[5], dt[6])        
        self._temperature = 0
        
        
    def getTurbidity(self):
        """Record turbidity
        Args:
            None
        Returns:
            None
        Raises:
            None
        """
        subject = 'Water'
        attribute = 'Turbidity'
        unit = 'NTU'
        sensor = 'turbidity'
        status_qualifier = 'Success'
        comment = ''
        
        
        from Turbidity import Turbidity
        tur = Turbidity()
        # Log temperature
        turbidity = 0
        try:
            turbidity = tur.NTU()

            status_qualifier = 'Success'
            if self.test:
                status_qualifier = 'Test'
            print("NTU", turbidity)
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            comment = str(e)

        self.save_Env(subject, attribute, "{:1.1f}".format(turbidity), unit, sensor, status_qualifier, comment)                
            
    def getEC(self):
        """Record electrical conductivity
        Args:
            None
        Returns:
            None
        Raises:
            None
        """
        from EC import EC
        
        subject = 'Water'
        attribute = 'EC'
        unit = 'ppm'
        sensor = 'ec'
        status_qualifier = 'Success'
        comment = ''
        
        ec_sensor = EC(self._temperature)
        # Log electrical conductivity
        ec = 0
        try:
            ec = ec_sensor.get()
            if self.test:
                status_qualifier = 'Test'
        except Exception as e:
            print("Exception", e)
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            comment = str(e)
        self.save_Env(subject, attribute, "{:1.1f}".format(ec), unit, sensor, status_qualifier, comment)                

    def getPressure(self):
        """Pressure, Temperature (and Humidity)
        Args:
            None
        Returns:
            None
        Raises:
            None
        """
        from BME280 import BME280
        from pyb import I2C
        i2c = I2C(1, I2C.MASTER)
        bme = BME280(i2c = i2c)
        
        comment = ''

        # Log electrical conductivity
        temperature = 0
        pressure = 0
        humidity = 0
        status_qualifier = 'Success'
        if self.test:
            status_qualifier = 'Test'
        try:
            temperature,pressure,humidity = bme.get_data()
            #print("T", temperature)

        except Exception as e:
            #print("Exception", e)
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            comment = str(e)

        self._temperature = temperature # save for EC compensation

        subject = 'Water'
        sensor = 'BME280'
        
        attribute = 'Pressure'
        unit = 'mbar'
        print("T2", temperature)        
        self.save_Env(subject, attribute, "{:1.1f}".format(pressure), unit, sensor, status_qualifier, comment)                
            
        attribute = 'Temperature'
        unit = 'C'
        self.save_Env(subject, attribute, "{:1.1f}".format(temperature), unit, sensor, status_qualifier, comment)                
            
        attribute = 'Humidity'
        unit = '%'
        self.save_Env(subject, attribute, "{:1.1f}".format(humidity), unit, sensor, status_qualifier, comment)                
            
    def log(self, test=False):
        '''Logsensors
            Uncomment desired sensors
            Imports are in the function to avoid loading unnecessary code
        '''
        print("In log")
        self.getPressure()
        print("Turbidity")
        self.getTurbidity()
        print("EC")
        self.getEC()
        # close file when done logging
        self._persist.close()
        
    def save_Env(self, subject, attribute, value, unit, sensor, status_qualifier, comment):        
        rec = ['Environment_Observation', self._id, self._ts, self._lat, self._long, subject, attribute, value, unit, sensor, status_qualifier, '']            
        # copy record
        print(rec)
        self._persist.save(rec)

def main():
    '''
        Function that should get called from scripts
    '''

    lg = LogSensors(env_file_name, env_header, Logger.INFO)
    lg.log()

def validate():
    '''
        Quick test to check working properly
    '''
    
    lg = LogSensors(env_file_name, env_header)
    lg.log()
    
def test():
    '''
        Use for debugging when need detailed output
    '''
    
    lg = LogSensors(env_file_name, env_header)
    lg.test = True
    lg.log()
    
