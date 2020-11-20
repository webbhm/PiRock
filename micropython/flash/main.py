"""
/flash/main.py

Initial setup and configuration
Should be called if there is no SD card inserted
Assumes variables are set in conf.py

Author: Howard Webb
Data: 11/13/2020

"""
import conf
from utime import sleep, ticks_ms, ticks_diff, localtime
import Environ
from pyb import RTC, LED
import Wifi

led_G = LED(2)
led_B = LED(3)
# Get a wifi connection
# Set the real time clock (RTC)
wifi = None


def set_time():
    print("Set NTP time")
    # Get NTP time, initialize env and set timer
    try:
    #try Exception as e:
        import ntptime
        ntptime.set_time()
    except Exception as e:
        print("Failure setting NTP time -", str(e))
        
        
def set_env():
    # Set the environmental variables
    Environ.create_env()
    
def set_timer():
    # Set the wake-up timer for periodic starting
    tm = conf.SAMPLE_MIN * 60 * 1000   # multiply by seconds per minute and miliseconds
    RTC().wakeup(tm)

def init_now():
    # Perform the initialization work
    global wifi
    led_B.off()
    if wifi is None:
        try:
            wifi = Wifi.connect()
        except:            
            print("Failure getting connection needed for setup, check SSID and PWD")
            return
    set_time()
    set_env()
    set_timer()
    # blue LED indicates successful setup
    led_B.on()

        
def init_later():
    # wait till reach start time
    led_B.off()
    tm = utime.localtime()
    min = tm[4]
    wait = (min - 1) * 60  # seconds to delay
    utime.sleep(wait)
    # count down the last seconds
    while min != conf.START_TIME:
        utime.sleep(1)
        tm = utime.localtime()
        min = tm[4]
    init_now()


# Default to wifi connection for using WebREPL
try:
    wifi = Wifi.connect()  # Comment out this line if not using WebREPL
    pass
except Exception as e:
    print("Failure getting connection needed for setup:", str(e))


