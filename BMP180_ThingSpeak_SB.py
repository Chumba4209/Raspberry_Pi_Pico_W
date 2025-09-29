import network
import urequests
import time
import machine
import bmp180
import ujson
import socket
from machine import reset

# Config
CONFIG_FILE = "wifi.json"
THINGSPEAK_URL = "http://api.thingspeak.com/update"
THINGSPEAK_API_KEY = "YOUR_API_KEY"  # could also be moved to portal if needed

# BMP180 Setup
i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))  # D1=GPIO5, D2=GPIO4
sensor = bmp180.BMP180(i2c)
sensor.oversample_sett = 2
sensor.baseline = 101325   # sea-level pressure reference

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
    ap.config(essid="ESP_BMP180_Config", password="12345678")

    print("AP started → connect to WiFi 'ESP_BMP180_Config', open http://192.168.4.1")

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
                    print("WiFi credentials saved. Rebooting...")
                    time.sleep(2)
                    reset()
            except Exception as e:
                print("Error parsing:", e)
        else:
            html = """<!DOCTYPE html>
<html>
  <head><title>BMP180 WiFi Setup</title></head>
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
        print("No WiFi config, starting portal...")
        start_config_portal()

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(cfg["ssid"], cfg["password"])

    print("Connecting to", cfg["ssid"])
    for _ in range(20):  # wait up to 20s
        if wlan.isconnected():
            print("Connected:", wlan.ifconfig())
            return wlan
        time.sleep(1)

    print("WiFi connect failed, starting portal...")
    start_config_portal()

# ThingSpeak Upload
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

# Main
wlan = connect_wifi()

while True:
    temp = sensor.temperature   # °C
    pressure = sensor.pressure  # Pa
    
    print("Temperature: {:.2f} C, Pressure: {:.2f} Pa".format(temp, pressure))
    upload_data(temp, pressure)
    
    time.sleep(15)  # ThingSpeak minimum upload interval
