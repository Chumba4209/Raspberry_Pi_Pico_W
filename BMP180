from machine import Pin, SoftI2C
from bmp085 import BMP180
import time

i2c = SoftI2C(sda = Pin(20), scl = Pin(21))
print("I2C", i2c.scan())

bmp = BMP180(i2c)
bmp.oversample = 2
bmp.sealevel = 1010.5

while True: 
  tempC = bmp.temperature    #get the temperature in degree celsius
  pres_hPa = bmp.pressure    #get the pressure in hpa
#   altitude = bmp.altitude    #get the altitude
  temp_f = (tempC * (9/5) + 32)  #convert the temperature value in fahrenheit
  print(str(tempC) + "°C " + str(temp_f) + "°F " + str(pres_hPa) + "hPa ")
  time.sleep_ms(100)  #delay of 100 milliseconds
