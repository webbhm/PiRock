# PiRock
PiRock is a fork of Oregon State University's [Smart Rock](http://www.open-sensing.org/smart-rock), a low cost (under $200) steam monitoring sensor package that collects:
* water depth (via a pressure sensor)
* temperature
* electrical conductivity (water hardness)
* turbidity
Where the Smart Rock is built around an Arduino core, the PiRock is built around the Raspberry Pi.  Other than this change, the housing and sensors are the same.
## Reason for Change
From work on several hydroponic projects ([MVP](https://https://github.com/futureag/blog/wiki)/[MarsFarm](https://marsfarm.io/)) and an [autonomous boat](https://github.com/cloudmesh-community/boat), I have come to prefer the Raspberry Pi environment over Arduino.  I like the ability to develop code on the same platform where it will be implemented, and using standard programming languages like Pyton instead of a proprietary language.  The Arduino does have some advantages such as native analog pin support, but most of these advantages can easily be worked around.
The Smart Rock is part of [OPEnS](http://www.open-sensing.org/projects) Lab's ecology of projects built around the LOOM modular infrastructure.  Since I am not interested in the larger ecosystem, I felt free to start with a clean slate.  In addition, I have already worked with most of these sensors in the Raspberry Pi environment and would have no trouble integrating them there.
The other factor is the cost and complexity of the Smart Rock build.  Custom PCB boards need to fabricated and individual components soldered. The Arduino requires additional resources:
* Real time clock
* SD card reader
* WiFi
The Arduino has two big advantages:
* It includes analog GPIO pins for easy integration of voltage sensors (electrical eonductivity meter and turbidity meter)
* 'Sleep' mode is native; the ability to put the Arduino into a low power state that conserves battery power.  The Raspberry Pi is always on and will drain a battery in several hours, the Arduino can be put to sleep and only activated momentarily to take sensor readings, allowing a battery to last for months.  There are however easy hardware additions for the Raspberry Pi that solve both of these issues.
## Raspberry Pi Hardware
The core of the PiRock 'brains' is a Raspberry Pi Zero W.  The smallest version of the Raspberry Pi but with WiFi built in.
Analog sensors are managed with an ADC (analog to digital converter), a [$7 circuit](https://www.amazon.com/s?k=Analog+digital+chip&ref=nb_sb_noss_2) that takes digital input and gives I2C output.  I2C is a standard protocol bus found on both the Arduino and Raspberry Pi.  This is used by both designs for communication with the pressure sensor.  With the PiRock, all sensor communications are now over the I2C.
Sleep mode (and a real-time clock) are added via a [Witty Pi 3](https://www.robotshop.com/en/witty-pi-3-rtc-power-management-raspberry-pi-boards.html) board.  This card manages the power to the Raspberry Pi, shutting down and starting it up for sensor readings.
The rest of the build, housing and sensors is bsically the same; though I have traded out the pressure sensor and custom PCB with a pre-build circuit board.  It costs a bit more but saves time and effort.
