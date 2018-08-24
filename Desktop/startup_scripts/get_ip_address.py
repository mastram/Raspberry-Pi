from sense_hat import SenseHat
import socket
import fcntl
import struct

def get_ip_address(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915, # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
            )[20:24])

sense = SenseHat()
try:
    wlan_ip = get_ip_address('wlan0')
    sense.show_message("wlan0 : " + wlan_ip,scroll_speed = 0.10)
except:
     sense.show_message("No wlan0",scroll_speed = 0.10)

try:
    eth_ip = get_ip_address('eth0')
    sense.show_message("eth0 : " + eth_ip,scroll_speed = 0.10)
except:
     sense.show_message("No eth0",scroll_speed = 0.10)

