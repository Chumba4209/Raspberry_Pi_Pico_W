#Main DHT22 with WiFiManager + ThingSpeak
import network
import urequests
import time
import machine
import dht
import wifi_manager  # WiFiManager module (wifi_manager.py must be in device)

# ThingSpeak configuration
THINGSPEAK_API_KEY = "YOUR_API_KEY"   # Change in portal
THINGSPEAK_URL = "http://api.thingspeak.com/update"

# DHT22 sensor pin
dht_pin = machine.Pin(4)   # GPIO4 (D2 on NodeMCU)
sensor = dht.DHT22(dht_pin)

#Main Connect to WiFi using WiFiManager
print("Starting WiFiManager...")
wlan, config = wifi_manager.connect()   # Opens portal if no credentials

#Main Upload function
def upload_data(temp, hum):
    api_key = config.get("api_key", THINGSPEAK_API_KEY)  # Allow API override
    url = "{}?api_key={}&field1={:.2f}&field2={:.2f}".format(
        THINGSPEAK_URL, api_key, temp, hum
    )
    try:
        response = urequests.get(url)
        print("ThingSpeak response:", response.text)
        response.close()
    except Exception as e:
        print("Upload failed:", e)

#Main Loop
while True:
    try:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        
        print("Temp: {:.2f} °C, Humidity: {:.2f} %".format(temperature, humidity))
        
        upload_data(temperature, humidity)
    except Exception as e:
        print("Sensor error:", e)
    
    time.sleep(15)  # ThingSpeak requires at least 15s delay
