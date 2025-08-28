import machine
import onewire
import ds18x20
import time
import ssd1306 

datapin = machine.Pin(4)  
i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))  # adjust pins as needed
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

ds_sensor = ds18x20.DS18X20(onewire.OneWire(datapin))

roms = ds_sensor.scan()
print('Found DS18B20 device(s):', roms)

while True:
    ds_sensor.convert_temp()
    time.sleep_ms(750)  
    
    oled.fill(0) 
    for rom in roms:
        temp = ds_sensor.read_temp(rom)
        print("Temperature:", temp, "°C")
        
        # Display on OLED
        oled.text("DS18B20 Sensor", 5, 10)
        oled.text("Temp: {:.2f} C".format(temp), 5, 30)
    
    oled.show()
    time.sleep(2)
