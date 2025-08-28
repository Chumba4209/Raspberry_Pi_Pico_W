import network
import time
import urequests
from machine import I2C, Pin
import bh1750

WIFI_SSID = ""
WIFI_PASSWORD = ""


# Replace with your Firebase Realtime Database URL 
FIREBASE_URL = ""
FIREBASE_SECRET = "YOUR_DATABASE_SECRET"   # From Firebase console -> Project Settings -> Service accounts -> Database secrets

i2c = I2C(0, scl=Pin(22), sda=Pin(21))  # adjust pins if needed
sensor = bh1750.BH1750(i2c)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    print("Connecting to WiFi...", end="")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.5)
    print("\nConnected! IP:", wlan.ifconfig()[0])

def send_to_firebase(lux_value):
    url = "{}BH1750.json?auth={}".format(FIREBASE_URL, FIREBASE_SECRET)
    data = {"Lux": lux_value}
    try:
        response = urequests.patch(url, json=data)
        print("Data sent:", data)
        response.close()
    except Exception as e:
        print("Error sending to Firebase:", e)

connect_wifi()

while True:
    lux = sensor.luminance(bh1750.BH1750.CONT_HIRES_1)
    print("Light Level: {:.2f} lx".format(lux))
    
    send_to_firebase(lux)
    
    time.sleep(10)  # send every 10s
