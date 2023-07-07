import network
import time
import socket
import machine
import connect

# Configure Wi-Fi credentials
SSID = connect.SSID
PASSWORD = connect.PASSWORD

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    time.sleep(1)

# IP addresses of the two Pico W boards
# Change these to the IP addresses of your Pico W boards
pico1_ip = "192.168.0.144"
pico2_ip = "192.168.0.152"

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to Pico W #2
server_address = (pico2_ip, 1234)
sock.connect(server_address)

# Configure onboard LED
led = machine.Pin('LED', machine.Pin.OUT)

while True:
    # Send data to Pico W #2
    message = "Hello from Pico W #1"
    sock.send(message.encode())

    # Receive data from Pico W #2
    data = sock.recv(1024)
    print("Received:", data.decode())

    # Toggle the onboard LED
    led.value(not led.value())

    # Add a delay between messages
    time.sleep(1)

sock.close()
