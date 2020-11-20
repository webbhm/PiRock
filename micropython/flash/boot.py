# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal

import pyb
import os, sys

#pyb.main('main.py') # main script to run after this one
#pyb.usb_mode('CDC+MSC') # act as a serial and a storage device
#pyb.usb_mode('CDC+HID') # act as a serial device and a mouse

if pyb.SDCard().present():
    pyb.usb_mode('VCP+MSC', msc=(pyb.SDCard(),)) # expose SD card to the PC

    os.mount(pyb.SDCard(), '/sd')
    sys.path[1:1] = ['/sd', '/sd/lib']
    print("SD Mounted")

if pyb.SDCard().present():
    # Try starting from the SD card
    pyb.main('/sd/smain.py') # main script to run after this one
    print("Started /sd/smain.py")
else:
    # If that fails (no SD card), start the flash
    pyb.main('/flash/main.py') # main script to run after this one
    print("Started /flash/main.py")
    
   
