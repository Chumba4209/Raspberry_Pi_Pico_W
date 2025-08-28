from machine import Pin
from time import sleep
import dht

dataPin = Pin(2,Pin.IN,Pin.PULL_UP)
sensor = dht.DHT22(dataPin)
print('DT22 Sensor data')
while True:
    sensor.measure()
    tempC=sensor.temperature()
    hum=sensor.humidity()
    print(tempC)
    print(hum)
    sleep(1)
