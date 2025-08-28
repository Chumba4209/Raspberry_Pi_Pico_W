from machine import Pin, SoftI2C
from bmp085 import BMP180
import ssd1306
import time

# I2C setup (adjust SDA/SCL pins if different for your board)
i2c = SoftI2C(sda=Pin(20), scl=Pin(21))
print("I2C devices found:", i2c.scan())

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

bmp = BMP180(i2c)
bmp.oversample = 2
bmp.sealevel = 1010.5   # adjust this value based on your location

while True:
    try:
        tempC = bmp.temperature
        pres_hPa = bmp.pressure
        #temp_f = (tempC * 9/5) + 32
        # altitude = bmp.altitude   # Uncomment if you want altitude too

        print(str(tempC) + "°C " + str(temp_f) + "°F " + str(pres_hPa) + " hPa")

        oled.fill(0)  # clear screen
        oled.text("BMP180 DATA", 0, 0)
        oled.text("Temp: " + str(round(tempC, 1)) + " C", 0, 16)
       #oled.text("Temp: " + str(round(temp_f, 1)) + " F", 0, 26)
        oled.text("Pres: " + str(round(pres_hPa, 1)) + " hPa", 0, 36)
        # oled.text("Alt: " + str(round(altitude, 1)) + " m", 0, 46)
        oled.show()

        time.sleep(2)

    except OSError as e:
        print("Sensor error:", e)
