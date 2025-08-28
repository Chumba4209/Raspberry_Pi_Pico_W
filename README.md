
# IoT Sensor Projects with MicroPython

This repository contains various MicroPython projects demonstrating how to connect different sensors to Raspberry Pi Pico W boards and push their data to cloud platforms like **Adafruit IO, ThingSpeak, and Firebase**. 

##  Supported Sensors

* **BMP180** → Temperature & Pressure
* **BH1750** → Light Intensity
* **DHT11** → Temperature & Humidity
* **DS18B20** → Waterproof Temperature Sensor
* **PIR** → Motion Detection

Each sensor has a standalone script that connects to WiFi, reads sensor values, and publishes the data to a chosen cloud service.

##  OLED Display (SSD1306 - 0.96")

The OLED (128x64, I²C) is used to show real-time readings locally before or alongside sending them to the cloud.

Typical display:

* Sensor Name
* Value (Temperature, Pressure, etc.)
* Units

This gives immediate feedback, making debugging and demonstrations easier.

---

##  Platform Integrations

### 1. Adafruit IO (MQTT)

* Requires **Adafruit IO Username** and **AIO Key**.
* Data is published using MQTT topics for each sensor.
* Example: BMP180 publishes `Temperature` and `Pressure` readings.

---

### 2. ThingSpeak (HTTP API)

* Requires **ThingSpeak Channel ID** and **API Key**.
* Data is sent via HTTP GET requests.
* Example: DHT11 sends Temperature to **field1** and Humidity to **field2**.

---

### 3. Firebase (REST API / Firestore)

* Requires:

  * API Key
  * Project ID
  * User Email
  * User Password
* Data is structured into Firestore documents with fields such as `Temperature`, `Pressure`, `Humidity`, etc.
* Example: DS18B20 sends temperature readings to `EspData/DS18B20`.

---

##  Project Structure

```
/sensors
   bmp180.py        # BMP180 sensor to Adafruit/ThingSpeak/Firebase
   bh1750.py        # BH1750 sensor to Adafruit/ThingSpeak/Firebase
   dht11.py         # DHT11 sensor to Adafruit/ThingSpeak/Firebase
   ds18b20.py       # DS18B20 sensor to Adafruit/ThingSpeak/Firebase
   pir.py           # PIR sensor to Adafruit/ThingSpeak/Firebase

/oled
   oled_display.py  # General SSD1306 OLED usage examples

/platforms
   adafruit.py      # MQTT publishing example
   thingspeak.py    # ThingSpeak publishing example
   firebase.py      # Firebase REST API publishing example
```

---

## 🔧 Requirements

* **Board:** Raspberry Pi pico W
* **Firmware:**Thonnyy IDE
* **Libraries:**

  * `umqtt.simple` (for Adafruit MQTT)
  * `urequests` (for ThingSpeak & Firebase HTTP)
  * `ssd1306` (for OLED)
  * Sensor drivers: `bmp180`, `bh1750`, `dht`, `onewire`, `ds18x20`

---

##  Getting Started

1. Clone or download this repository..
3. Upload the relevant sensor file using **Thonny** or **ampy**.
4. Edit Wi-Fi credentials and platform keys inside the script.
5. Run the script to start sending sensor data.

---

##  Example Workflow

1. **Read data** from BMP180 → `Temperature = 25.4 °C, Pressure = 1002 hPa`.
2. **Display** values on OLED.
3. **Send** values to:

   * Adafruit IO (MQTT topic)
   * ThingSpeak (HTTP request fields)
   * Firebase (Firestore document)

---

## ✅ Future Work

* Create a unified configuration portal for Wi-Fi & API keys.

