#Main DS18B20 with WiFiManager + ThingSpeak
import network
import urequests
import time
import machine
import onewire
import ds18x20
import wifi_manager  

# ThingSpeak configuration
THINGSPEAK_API_KEY = "YOUR_API_KEY"   # Edited via WiFiManager portal
THINGSPEAK_URL = "http://api.thingspeak.com/update"

#Main Setup DS18B20 sensor
ds_pin = machine.Pin(4)   # GPIO4 (D2 on NodeMCU, adjust if needed)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
roms = ds_sensor.scan()
print("Found DS18B20 devices:", roms)

#Main Connect WiFi via WiFiManager
print("Starting WiFiManager...")
wlan, config = wifi_manager.connect()   # Launches captive portal if no credentials

#Main Upload function
def upload_data(temp):
    api_key = config.get("api_key", THINGSPEAK_API_KEY)  # API key override
    url = "{}?api_key={}&field1={:.2f}".format(
        THINGSPEAK_URL, api_key, temp
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
        ds_sensor.convert_temp()
        time.sleep_ms(750)   # Wait for conversion to complete
        
        for rom in roms:
            temperature = ds_sensor.read_temp(rom)
            print("Temperature: {:.2f} °C".format(temperature))
            upload_data(temperature)
            
    except Exception as e:
        print("Sensor error:", e)
    
    time.sleep(15)  # ThingSpeak requires minimum 15s delay
