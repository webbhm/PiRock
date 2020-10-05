"""
Test of the Turbidity meter using an ADC
# The Turbidity sensor mapped from 0 to 1023 (0 - 5 volts)
# ADC maps values -32768 to 32767, GND is 0 (-5 - 5 v)
# Voltage conversion is volts = (reading / 32767) * 5
# This may need some calibration adjustment
"""
from __future__ import print_function
# Import the ADS1x15 module.
from ADS1115 import ADS1115

in_voltage = 5
adc_range = 32767
clear_voltage = 2.85 # voltage read from clear water


class Turbidity(object):
    """
    Turbidity meter
    """

    def __init__(self):
        """
        initialize the turbidity meter
        """
        self._adc = ADS1115()
        self._id = 1 # Pin 1 of the ADC
        self._gain = 1

    def get(self):
        """
        returns the raw values of the turbidity meter
        :return:
        """
        return self._adc.volts5(self._id)
    
    def NTU(self):
        volts = self.get()
        if volts <= 2.5:
            return 3000
        
        return (-1120.4 * (volts**2)) + (5742.3 * volts) - 4352.9   
        # Taken from wiki.dfrobot.com/Turbidity_sensor_SKU_SEN0189
        # ntu = -1120.4 * square(volts) + 5742.3 * volts - 4352.9


def test():
    print("Turbidity Test")
    turbidity = Turbidity()
    value = turbidity.get()
    print("Turbidity", value)

def test2():
    turbidity = Turbidity()
    volts = turbidity.get()
    value = turbidity.NTU()
    print("Turbidity Volts", volts,  "NTU", value)



if __name__ == "__main__":
    test2()
