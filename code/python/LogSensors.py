'''
Log Sensors to CSV file
Called from /home/pi/scripts/LogSensors.sh - needs to be uncommented for to run
Author: Howard Webb
Date: 9/28/2020
'''

from LogUtil import Logger
from CSV_Util import CSV_Util
from getmac import get_mac_address
from datetime import datetime

class LogSensors(object):

    def __init__(self, lvl=Logger.INFO, file="/home/pi/logs/obsv.log"):
        """Record optional sensor data
        Args:
            lvl: Logging level
        Returns:
            None
        Raises:
            None
        """        
        self._logger = Logger("LogSensors", lvl)
        self._activity_type = "Environment_Observation"
        self._persist = CSV_Util()
        self.test = False
        self._mac = get_mac_address()
        self._ts = datetime.isoformat(datetime.now())
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
        from Turbidity import Turbidity
        tur = Turbidity()
        # Log temperature
        self._logger.info("Turbidity")                
        try:
            turbidity = tur.get()

            status_qualifier = 'Success'
            if self.test:
                status_qualifier = 'Test'
            rec = ['Environment_Observation', self._mac, self._ts, 'Water', 'Turbidity', "{:10.1f}".format(turbidity), 'NTU', 'turbidity', status_qualifier, '']            
            # copy record
            self._persist.save(rec)
            self._logger.debug("{}, {}, {:10.1f}".format("turbidity", status_qualifier, turbidity))
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            rec = ['Environment_Observation', self._mac, self._tx, 'Water', 'Turbidity', '', 'NTU', 'turbidity', status_qualifier, str(e)]
            self._persist.save(rec)            
            self._logger.error("{}, {}, {}".format("turbidity", turbidity, e))

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
        ec = EC()
        # Log electrical conductivity
        self._logger.info("EC")                
        try:
            ec = ec.getEC()
            status_qualifier = 'Success'
            if self.test:
                status_qualifier = 'Test'
            rec = ['Environment_Observation', self._mac, self._ts, 'Water', 'EC', "{:10.1f}".format(ec), 'ppm', 'ec', status_qualifier, '']            
            # copy record
            self._persist.save(rec)
            self._logger.debug("{}, {}, {:10.1f}".format("EC", status_qualifier, ec))
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            rec = ['Environment_Observation', self._mac, self._ts, 'Water', 'EC', '', 'ppm', 'ec', status_qualifier, str(e)]
            self._persist.save(rec)            
            self._logger.error("{}, {}, {}".format("EC", ec, e))

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
        bme = BME280()  

        # Log electrical conductivity
        self._logger.info("Pressure")                
        try:
            temperature,pressure,humidity = bme.getData()
            self._temperature = temperature # save for EC compensation
            status_qualifier = 'Success'
            if self.test:
                status_qualifier = 'Test'
            rec = ['Environment_Observation', self._mac, self._ts, 'Water', 'Pressure', "{:10.1f}".format(pressure), 'mbar', 'BME280', status_qualifier, '']            
            # copy record
            self._persist.save(rec)
            self._logger.debug("{}, {}, {:10.1f}".format("Pressure", status_qualifier, pressure))
            
            rec = ['Environment_Observation', self._mac, self._ts, 'Water', 'Temperature', "{:10.1f}".format(temperature), 'C', 'BME280', status_qualifier, '']            
            # copy record
            self._persist.save(rec)
            self._logger.debug("{}, {}, {:10.1f}".format("Temperature", status_qualifier, temperature))

        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            rec = ['Environment_Observation', self._mac, self._ts, 'Water', 'Pressure', '', 'mbar', 'BME280', status_qualifier, str(e)]
            self._persist.save(rec)            
            self._logger.error("{}, {}, {}".format("Pressure", pressure, e))

            rec = ['Environment_Observation', self._mac, self._ts, 'Water', 'Temperature', '', 'C', 'BME280', status_qualifier, str(e)]
            self._persist.save(rec)            
            self._logger.error("{}, {}, {}".format("Temperature", temperature, e))
            
    def log(self, test=False):
        '''Logsensors
            Uncomment desired sensors
            Imports are in the function to avoid loading unnecessary code
        '''

        self.getPressure()        
        self.getTurbidity()
        self.getEC()
        
        
def main():
    '''
        Function that should get called from scripts
    '''

    lg = LogSensors(Logger.INFO)
    lg.log()

def validate():
    '''
        Quick test to check working properly
    '''
    
    lg = LogSensors(Logger.DEBUG)
    lg.log()
    
def test():
    '''
        Use for debugging when need detailed output
    '''
    
    lg = LogSensors(Logger.DETAIL)
    lg.test = True
    lg.log()

if __name__=="__main__":
    #main()
    test()
