import socket
import time

UDP_IP = "169.254.116.33" #This needs to be the Pi's IP
UDP_PORT = 5005
#MESSAGE = b'2000'
MESSAGE = "Hello"


print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)
print ("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
#sock.bind((UDP_IP, UDP_PORT))
#sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
#sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

#sock.bind((UDP_IP, UDP_PORT))
count=1
while True:
    time.sleep(1)
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
    #data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    #print ("received message:", data)
    print(count)
    count=count+1