import machine
import time
import ssd1306

BUTTON_PIN = 7   # Adjust based on your board
SCL_PIN = 10     # I2C clock pin
SDA_PIN = 8      # I2C data pin

button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

i2c = machine.I2C(0, scl=machine.Pin(SCL_PIN), sda=machine.Pin(SDA_PIN))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def is_long_press(pin, duration=1000):
    press_time = time.ticks_ms()
    while pin.value() == 0:   # 0 = pressed (since pull-up is used)
        if time.ticks_diff(time.ticks_ms(), press_time) > duration:
            return True
    return False

def show_message(line1, line2):
    oled.fill(0)  # clear screen
    oled.text(line1, 40, 30)
    oled.text(line2, 40, 40)
    oled.show()

while True:
    if button.value() == 0:   # Button pressed
        if is_long_press(button):
            show_message("Long", "pressed")
            time.sleep(0.5)
        else:
            show_message("Switch", "pushed")
            time.sleep(1)
    else:
        show_message("Switch", "released")
        time.sleep(0.5)
