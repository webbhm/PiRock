"""
Make a wifi connection and get the NTP time
May need to change for wifi login info issues
Author: Howard Webb
Date: 11/6/2020

Wifi has issues, note changes for soft reset
github.com/micropython/micropython/issues/4681
"""

try:
    import usocket as socket
except:
    import socket
try:
    import ustruct as struct
except:
    import struct
    
import machine
import utime
from pyb import RTC

# (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
NTP_DELTA = 3155673600

# The NTP host can be configured at runtime by doing: ntptime.host = 'myhost.org'
host = "pool.ntp.org"


def time():
    # get the NTP time from the website
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(2)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    return val - NTP_DELTA


# There's currently no timezone support in MicroPython, and the RTC is set in UTC time.
def settime():
    # Set the RTC to the NTP time
    print("Set Time")
    t = time()
    tm = utime.localtime(t)
    print("NTP", tm)
    RTC().datetime((tm[0], tm[1], tm[2], tm[6], tm[3], tm[4], tm[5], 0))
    
def connect():    
    # Connect to network and set the time
    import network, pyb, time
    red = pyb.LED(1)
    green = pyb.LED(2)

    SSID = "WebbRouterNet-2.4"
    PWD = "ILoveRhonda"

    wifi = network.WLAN(network.STA_IF)
    wifi.config(trace=0)
    while True:
        wifi.active(True)
        wifi.connect(SSID, PWD)
        red.on()
        time.sleep(0.2)
        t0 = time.ticks_ms()
        while wifi.status() in (1, 2) and time.ticks_diff(time.ticks_ms(), t0) < 10000:
            time.sleep(1)
        if wifi.isconnected():
            break
        wifi.deinit()
        print('Retry Connection')
        red.off()
        time.sleep(0.5)
        red.on()
    print('Connected')
    red.off()
    green.on()
        
    settime()
    print(utime.localtime())
    wifi.disconnect()
 
