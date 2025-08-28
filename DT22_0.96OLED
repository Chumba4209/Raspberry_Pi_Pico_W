import dht
from machine import Pin, SoftI2C
from time import sleep
import ssd1306

#Pin assignment 
i2c = SoftI2C(scl=Pin(21), sda=Pin(20))

oled_width = 128
oled_height = 64
print("I2C Scan: ", i2c.scan())
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

sensor = dht.DHT22(Pin(2))

while True:
    try:
        sensor.measure()
        print("Temp:", sensor.temperature(), "C")
        print("Humidity:", sensor.humidity(), "%")
        oled.text("DHT SENSOR DATA", 0,0)
        oled.text('Temp: ' + str(sensor.temperature()) + " C", 0, 20)
        oled.text('Hum: '+ str(sensor.humidity()) + "%", 0, 30)
        oled.show()
        sleep (3)

    except OSError as e:
        print("Failed to read sensor:", e)
        
