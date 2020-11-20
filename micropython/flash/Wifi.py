import network
import pyb
import conf
import time


led_G = pyb.LED(2)
led_B = pyb.LED(3)
 
def connect(ssid=conf.SSID, pwd=conf.PWD):    
    # Connect to network
    led_G.on()

    wifi = network.WLAN(network.STA_IF)
    wifi.config(trace=0)
    while True:
        wifi.active(True)
        wifi.connect(ssid, pwd)
        led_G.on()
        time.sleep(0.2)
        t0 = time.ticks_ms()
        while wifi.status() in (1, 2) and time.ticks_diff(time.ticks_ms(), t0) < 10000:
            time.sleep(1)
        if wifi.isconnected():
            break
        wifi.deinit()
        print('Retry Connection')
        led_G.off()
        time.sleep(0.5)
    print('Connected at:', wifi.ifconfig()[0])
    led_G.on()
    return wifi
