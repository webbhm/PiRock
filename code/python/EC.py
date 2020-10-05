import time
# Import the ADS1x15 module (analog to digital converter).
from ADS1115 import ADS1115
from LogUtil import Logger

class EC(object):
    
   def __init__(self, temperature=25, logger=None):
      self._pin = 0 # ADS1115 Channel to use
      self._logger = logger
      if logger == None:
          self._logger = Logger("EC", Logger.INFO)
      # Create an ADS1115 ADC (16-bit) instance.
      self._adc = ADS1115(logger)
      self._temp = temperature
      self._tempCoeff = self.tempCoeff()

   def get(self):
        volts = self._adc.volts5(self._pin) * 1000  # uses mVolts
        coef_volt = volts/self._tempCoeff
        #self._logger.debug("Volts Raw" + str(volts) + "Coeff" + str(coef_volt))
        self._logger.info("{}: {}, {}: {}".format("mVolts Raw", volts, "Coeff", coef_volt))        
        if coef_volt < 150: # No solution
            self._logger.info("{} {}".format("No Solution: Voltage",coef_volt))
            return 0
        elif coef_volt > 3300:
            self._logger.info("Out of Range: Voltage" + str(coef_volt))
            return 0
        
        if coef_volt <= 448:
            ec_cur = 6.84 * coef_volt - 64.32
        elif coef_volt <=1457:
            ec_cur = 6.98 * coef_volt - 127
        else:
            ec_cur = 5.3 * coef_volt + 2278
        ec_cur = ec_cur/1000  # convert us/cm to ms/cm
        return ec_cur
        
   def tempCoeff(self):
       return 1.0 + 0.0185 * (self._temp - 25.0)
    
def test():
    print("Test EC")
    ec = EC()
    while True:
        value=ec.get()
        time.sleep(0.5)
        
if __name__ == "__main__":
    test()    