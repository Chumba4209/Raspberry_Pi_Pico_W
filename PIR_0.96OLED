from machine import Pin, SoftI2C
import ssd1306
import time

# Adjust SDA and SCL pins to your board wiring
i2c = SoftI2C(scl=Pin(21), sda=Pin(20))  
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

PIR_PIN = 7   # Change to the GPIO where PIR OUT is connected
pir = Pin(PIR_PIN, Pin.IN)

while True:
    motionDetected = pir.value()   # 1 if motion detected, 0 otherwise
    
    oled.fill(0)   # Clear OLED before writing
    
    oled.text("PIR SENSOR", 20, 0)
    
    if motionDetected == 1:
        oled.text("Motion", 30, 25)
        oled.text("Detected!", 25, 40)
        print("Motion Detected!")
    else:
        oled.text("No Motion", 25, 25)
        oled.text("Detected", 30, 40)
        print("No Motion")
    
    oled.show()
    time.sleep(1)   # update every second
