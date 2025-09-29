#Main PIR Sensor with WiFiManager + ThingSpeak
import network
import urequests
import time
import machine
import wifi_manager  

# ThingSpeak configuration
THINGSPEAK_API_KEY = "YOUR_API_KEY"   
THINGSPEAK_URL = "http://api.thingspeak.com/update"

#Main Setup PIR sensor
pir_pin = machine.Pin(14, machine.Pin.IN)  # GPIO14 (D5 on NodeMCU)

#Main Connect WiFi via WiFiManager
print("Starting WiFiManager...")
wlan, config = wifi_manager.connect()   # Opens portal if no saved credentials

#Main Upload function
def upload_data(motion_detected):
    api_key = config.get("api_key", THINGSPEAK_API_KEY)  # API key override
    url = "{}?api_key={}&field1={}".format(
        THINGSPEAK_URL, api_key, motion_detected
    )
    try:
        response = urequests.get(url)
        print("ThingSpeak response:", response.text)
        response.close()
    except Exception as e:
        print("Upload failed:", e)

#Main Loop
while True:
    motion = pir_pin.value()  # 1 = motion detected, 0 = no motion
    if motion:
        print("Motion Detected")
    else:
        print("No Motion")
        
    upload_data(motion)
    time.sleep(15)  
