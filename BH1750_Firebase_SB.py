#Main BH1750 with WiFiManager + Firebase
import network
import time
import urequests
from machine import I2C, Pin
import bh1750
import wifi_manager  

# Firebase config 
FIREBASE_URL = ""   # i.e "https://your-project-id.firebaseio.com/"
FIREBASE_SECRET = "YOUR_DATABASE_SECRET"

#Main Setup BH1750 sensor
i2c = I2C(0, scl=Pin(22), sda=Pin(21))  # GPIO22=SCL, GPIO21=SDA on ESP32
sensor = bh1750.BH1750(i2c)

#Main Connect WiFi using WiFiManager
print("Starting WiFiManager...")
wlan, config = wifi_manager.connect()   # Portal: WiFi SSID, password, Firebase URL & Secret

#Main Firebase upload function
def send_to_firebase(lux_value):
    fb_url = config.get("firebase_url", FIREBASE_URL)
    fb_secret = config.get("firebase_secret", FIREBASE_SECRET)
    
    if not fb_url or not fb_secret:
        print("Firebase config missing!")
        return
    
    url = "{}BH1750.json?auth={}".format(fb_url, fb_secret)
    data = {"Lux": lux_value}
    
    try:
        response = urequests.patch(url, json=data)
        print("Data sent:", data)
        response.close()
    except Exception as e:
        print("Error sending to Firebase:", e)

#Main Loop
while True:
    try:
        lux = sensor.luminance(bh1750.BH1750.CONT_HIRES_1)
        print("Light Level: {:.2f} lx".format(lux))
        send_to_firebase(lux)
    except Exception as e:
        print("Sensor error:", e)
    
    time.sleep(10)  
