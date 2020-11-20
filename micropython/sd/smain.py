"""
Called on power up from boot.py
Log sensors, turn off power, go back to sleep

Author: Howard Webb
Date: 11/13/2020

"""

from LogSensors import LogSensors
import machine
from pyb import Pin, LED, RTC, standby
from utime import sleep

led_R = LED(1)
led_G = LED(2)
led_B = LED(3)

def shut_down():
    #machine.deepsleep()
    # turn off power to I2C, USB and SD
    led_R.off()
    led_G.off()
    led_B.off()
    machine.Pin('EN_3V3').off()
    # put in deep sleep - clock will wake back up
    standby()

def write_line(line):
    #f = open('/sd/start_test.txt', 'a')
    dt = RTC().datetime()
    ts = "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}\n".format(dt[0], dt[1], dt[2], dt[4], dt[5], dt[6])        
    print(ts)
    print(line)

    #f.write(ts)
    #f.write(line + '\n')
    #f.close()

    sleep(.5)

def run():
    # Turn power on to I2C and pins
    Pin('EN_3V3').on()
    # Log the sensors
    ls = LogSensors()
    ls.log()
    # Go back to sleep
    shut_down()

# Core code that routes activities
    
if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    # This should be the primary function called when logging - keep at top of if statements
    # Alarm trigger - Log and go back to sleep
    write_line('DEEPSLEEP')
    run()

elif machine.reset_cause() == machine.PWRON_RESET:
    # Power turned on (battery plugged it) - start cycling 
    write_line('PWRON')
    for x in range(0, 5):
        led_G.toggle()
        sleep(.5)
    led_G.off()
    led_B.on()
    sleep(1)
    shut_down()

elif machine.reset_cause() == machine.HARD_RESET:
    # Button pressed - start wifi so can get into pyboard
    write_line('HARD')
    import Wifi
    Wifi.connect()

elif machine.reset_cause() == machine.SOFT_RESET:
    # CTL-D entered from the prompt - used for clearing memory while testing code
    write_line('SOFT')

elif machine.reset_cause() == machine.WDT_RESET:
    # Pin reset - may be used in the future for hotspot wifi data download
    # Not used at this time
    write_line('WDT')
else:        
    write_line("Unknown")