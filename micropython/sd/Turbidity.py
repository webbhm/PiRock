"""
Test of the Turbidity meter using an ADC
# The Turbidity sensor mapped from 0 to 1023 (0 - 5 volts)
# ADC maps values -32768 to 32767, GND is 0 (-5 - 5 v)
# Voltage conversion is volts = (reading / 32767) * 5
# This may need some calibration adjustment
"""

from pyb import ADC, Pin

# actual voltage is 3.3, but calculations are based on 5 volts
in_voltage = 5
adc_range = 4095
clear_voltage = 2.85 # voltage read from clear water


class Turbidity(object):
    """
    Turbidity meter
    """

    def __init__(self):
        """
        initialize the turbidity meter
        """
        self._adc = ADC(Pin.board.X6)

    def get(self):
        """
        returns the raw values of the turbidity meter
        :return:
        """
        volts = ((self._adc.read()/ adc_range) * in_voltage)
        return volts
    
    def NTU(self):
        volts = self.get()
        if volts <= 2.5:
            return 3000
        
        return (-1120.4 * (volts**2)) + (5742.3 * volts) - 4352.9   
        # Taken from wiki.dfrobot.com/Turbidity_sensor_SKU_SEN0189
        # ntu = -1120.4 * square(volts) + 5742.3 * volts - 4352.9

def calibrate():
    # Collect data for callibrating readings
    print("Turbidity Calibration")
    turbidity = Turbidity()

    t_header = 'NTU'

    # files to use
    t_dir = '/home/pi/python/PyRock/data/turbid.csv'

    # create files
    t_file = open(t_dir,'w')

    # write headers
    t_file.write(t_header)

    while True:
       value = turbidity.NTU()
       print("Turbidity NTU:", value)
       t_file.write(round(value, 2))
       time.sleep(2)

    t_file.close()

def run():
    # Test of continuous collection
    print("Turbidity Test")
    turbidity = Turbidity()
    while True:
        value = turbidity.NTU()
        print("Turbidity NTU:", value)
        time.sleep(2)

def test():
    # Validity test
    print("Turbidity Test")
    try:
        turbidity = Turbidity()
        volts = turbidity.get()
        value = turbidity.NTU()
        print("Turbidity Volts", volts,  "NTU", value)
    except Exception as e:
        print("ERROR: Failure reading Turbidity -", str(e))



#test2()
