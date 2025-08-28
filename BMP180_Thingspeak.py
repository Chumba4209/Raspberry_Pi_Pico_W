import network
import urequests
import time
import machine
import bmp180

WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASS = "YOUR_WIFI_PASSWORD"

THINGSPEAK_API_KEY = "YOUR_API_KEY"
THINGSPEAK_URL = "http://api.thingspeak.com/update"

i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))  # GPIO5 = D1, GPIO4 = D2 on NodeMCU
sensor = bmp180.BMP180(i2c)
sensor.oversample_sett = 2
sensor.baseline = 101325   # sea-level pressure reference

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            time.sleep(1)
    print("Connected:", wlan.ifconfig())
    return wlan

def upload_data(temp, pressure):
    url = "{}?api_key={}&field1={:.2f}&field2={:.2f}".format(
        THINGSPEAK_URL, THINGSPEAK_API_KEY, temp, pressure
    )
    try:
        response = urequests.get(url)
        print("ThingSpeak response:", response.text)
        response.close()
    except Exception as e:
        print("Upload failed:", e)

wlan = connect_wifi()

while True:
    temp = sensor.temperature   # °C
    pressure = sensor.pressure  # Pa
    
    print("Temperature: {:.2f} C, Pressure: {:.2f} Pa".format(temp, pressure))
    
    upload_data(temp, pressure)
    
    time.sleep(15)  # ThingSpeak minimum upload interval
