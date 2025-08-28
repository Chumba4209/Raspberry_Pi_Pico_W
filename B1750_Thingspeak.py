import network
import urequests
import time
import machine
import bh1750

WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASS = "YOUR_WIFI_PASSWORD"

THINGSPEAK_API_KEY = "YOUR_API_KEY"
THINGSPEAK_URL = "http://api.thingspeak.com/update"

i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))  # GPIO5 = D1, GPIO4 = D2 on NodeMCU
sensor = bh1750.BH1750(i2c)

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

def upload_data(light_level):
    url = "{}?api_key={}&field1={:.2f}".format(
        THINGSPEAK_URL, THINGSPEAK_API_KEY, light_level
    )
    try:
        response = urequests.get(url)
        print("ThingSpeak response:", response.text)
        response.close()
    except Exception as e:
        print("Upload failed:", e)

wlan = connect_wifi()

while True:
    lux = sensor.luminance(bh1750.BH1750.CONT_HIRES_1)  # Continuous high-res mode
    print("Light Intensity: {:.2f} lx".format(lux))
    
    upload_data(lux)
    
    time.sleep(15)  # ThingSpeak minimum upload interval
