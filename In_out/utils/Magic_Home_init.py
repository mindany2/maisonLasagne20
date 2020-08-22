import sys
import socket
import time
from wifi import Cell, Scheme
import os

def send(text):
    ip = "10.10.123.3"
    port = 48899

    byte_array = convert_to_bytes(text)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((ip, port))
    s.send(byte_array)
    s.close()

def convert_to_bytes(message):
    encoded = ":".join("{:02x}".format(ord(c)) for c in message)
    encoded = encoded.split(':')

    values = ['0x' + s for s in encoded]
    values = [int(v,16) for v in values]
    values.append(13)
    
    return bytearray(values)

def initialize():
    
    send("AT+WSSSID="+"hifi")
    print("WiFi Set")
    time.sleep(0.5)
    
    send("AT+WSKEY=WPA2PSK,AES,"+"louloululu")
    print("Password Set")
    time.sleep(0.5)

    send("AT+WMODE=STA")
    print("Switching to station mode")
    time.sleep(0.5)

    send("AT+Z")
    print("Disconnected")

def change_wifi_file(ssid):
    fichier = open("/etc/wpa_supplicant/led_test","r")
    contenu = fichier.read().split("\n")
    fichier.close()
    print(contenu)
    contenu[5] = "ssid=\""+ssid+"\""
    final = ""
    for ligne in contenu:
        final += ligne + "\n"
    fichier = open("/etc/wpa_supplicant/led_test","w")
    fichier.write(final)
    fichier.close()

    os.system("cp /etc/wpa_supplicant/led_test /etc/wpa_supplicant/wpa_supplicant.conf")

def reload_wifi():
    os.system("dhclient -r wlan0")
    os.system("sudo ifdown wlan0")
    time.sleep(2)
    os.system("sudo ifup wlan0")
    os.system("dhclient -v wlan0")

    os.system("echo \n iwconfig wlan0")

def check_for_reset():
    cells = Cell.all('wlan0')
    for cell in cells:
        if cell.ssid.count("LEDnet"):
            print(cell.ssid)
            change_wifi_file(cell.ssid)
            reload_wifi()
            initialize()

    os.system("cp /etc/wpa_supplicant/hifi /etc/wpa_supplicant/wpa_supplicant.conf")
    reload_wifi()


if __name__ == '__main__':
    check_for_reset()
