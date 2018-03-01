import socket
import time

UDP_IP = "169.254.89.200"
UDP_PORT = 8888
#MESSAGE = b'2000'
MESSAGE = "Hello"


print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)
print ("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
#sock.bind((UDP_IP, UDP_PORT))
#sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

#sock.bind((UDP_IP, UDP_PORT))

while True:
    time.sleep(5)
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print ("received message:", data)