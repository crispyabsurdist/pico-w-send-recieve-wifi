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

# Bind the socket to Pico W #2 IP address
server_address = (pico2_ip, 1234)
sock.bind(server_address)
sock.listen(1)

# Wait for a connection from Pico W #1
conn, addr = sock.accept()
print("Connected with Pico W #1")

# Configure onboard LED
led = machine.Pin('LED', machine.Pin.OUT)

while True:
    # Receive data from Pico W #1
    data = conn.recv(1024)
    print("Received:", data.decode())

    # Toggle the onboard LED
    led.value(not led.value())

    # Send response back to Pico W #1
    response = "LED toggled"
    conn.send(response.encode())

conn.close()
