import machine
import onewire
import ds18x20
import time

datapin = machine.Pin(4)  
ds_sensor = ds18x20.DS18X20(onewire.OneWire(datapin))

roms = ds_sensor.scan()
print('Found DS18B20 device(s):', roms)

while True:
    ds_sensor.convert_temp()
    time.sleep_ms(750)   # wait for conversion
    for rom in roms:
        temp = ds_sensor.read_temp(rom)
        print("Temperature:", temp, "°C")
    time.sleep(2)
