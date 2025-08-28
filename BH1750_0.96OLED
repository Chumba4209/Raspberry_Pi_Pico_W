from machine import Pin, SoftI2C
import ssd1306
import time
import bh1750   # Make sure bh1750.py is in the lib/ folder

i2c = SoftI2C(scl=Pin(21), sda=Pin(20))
print("I2C devices found:", i2c.scan())

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

sensor = bh1750.BH1750(i2c)
while True:
    lux = sensor.luminance(bh1750.BH1750.CONT_HIRES_1)
    print("Light Level:", lux, "lx")

    oled.fill(0)
    oled.text("BH1750 SENSOR", 15, 0)
    oled.text("Light:", 20, 25)
    oled.text(str(round(lux, 2)) + " lx", 20, 40)
    oled.show()

    time.sleep(2)
