from machine import Pin, SoftI2C
import time
import bh1750   # Make sure bh1750.py is in the lib/ folder

i2c = SoftI2C(scl=Pin(21), sda=Pin(20))
print("I2C devices found:", i2c.scan())

sensor = bh1750.BH1750(i2c)

while True:
    lux = sensor.luminance(bh1750.BH1750.CONT_HIRES_1)
    print("Light Level:", lux, "lx")
    time.sleep(2)
