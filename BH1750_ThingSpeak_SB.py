from machine import Pin, SoftI2C, reset
import ssd1306
import time
import bh1750
import network
import socket
import ujson
import urequests

# OLED Setup
i2c = SoftI2C(scl=Pin(21), sda=Pin(20))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# BH1750 Setup
sensor = bh1750.BH1750(i2c)

# Config
CONFIG_FILE = "wifi.json"
THINGSPEAK_URL = "http://api.thingspeak.com/update"
THINGSPEAK_API_KEY = "YOUR_API_KEY"  # You can also move this to portal if needed

def oled_message(lines):
    oled.fill(0)
    y = 0
    for line in lines:
        oled.text(line, 0, y)
        y += 12
    oled.show()

# WiFi Config Handling
def read_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return ujson.load(f)
    except:
        return {}

def save_config(ssid, password):
    with open(CONFIG_FILE, "w") as f:
        ujson.dump({"ssid": ssid, "password": password}, f)

# WiFi Manager
def start_config_portal():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="ESP_Config_OLED", password="12345678")

    oled_message(["Config Portal", "SSID: ESP_Config_OLED", "Pass: 12345678", "Go: 192.168.4.1"])
    print("AP started, connect to WiFi 'ESP_Config_OLED' and go to http://192.168.4.1")

    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    while True:
        cl, addr = s.accept()
        request = cl.recv(1024).decode()
        if "GET /?ssid=" in request:
            try:
                params = request.split(" ")[1]  # /?ssid=xxx&pass=yyy
                query = params.split("?")[1]
                kv = {}
                for pair in query.split("&"):
                    k, v = pair.split("=")
                    kv[k] = v
                ssid = kv.get("ssid")
                password = kv.get("pass")
                if ssid and password:
                    save_config(ssid, password)
                    response = "Saved! Rebooting..."
                    cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + response)
                    cl.close()
                    oled_message(["WiFi Saved!", "Rebooting..."])
                    time.sleep(2)
                    reset()
            except Exception as e:
                print("Error parsing:", e)
        else:
            html = """<!DOCTYPE html>
<html>
  <head><title>WiFi Setup</title></head>
  <body>
    <h2>Enter WiFi Credentials</h2>
    <form>
      SSID: <input type='text' name='ssid'><br>
      Password: <input type='password' name='pass'><br>
      <input type='submit' value='Save'>
    </form>
  </body>
</html>"""
            cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + html)
            cl.close()

def connect_wifi():
    cfg = read_config()
    if not cfg:
        oled_message(["No WiFi config", "Starting Portal..."])
        start_config_portal()

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(cfg["ssid"], cfg["password"])

    oled_message(["Connecting...", cfg["ssid"]])
    for _ in range(20):  # wait up to 20s
        if wlan.isconnected():
            ip = wlan.ifconfig()[0]
            oled_message(["Connected!", "IP: " + ip])
            print("Connected:", wlan.ifconfig())
            return wlan
        time.sleep(1)

    oled_message(["WiFi Failed", "Starting Portal..."])
    start_config_portal()

# ThingSpeak Upload
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

# Main
wlan = connect_wifi()

while True:
    lux = sensor.luminance(bh1750.BH1750.CONT_HIRES_1)
    print("Light Level:", lux, "lx")

    oled.fill(0)
    oled.text("BH1750 SENSOR", 10, 0)
    oled.text("Light:", 10, 25)
    oled.text(str(round(lux, 2)) + " lx", 10, 40)
    oled.show()

    upload_data(lux)
    time.sleep(15)
