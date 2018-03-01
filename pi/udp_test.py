import socket

UDP_IP = "169.254.116.33" #The Pi's IP
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, #internet
                     socket.SOCK_DGRAM) #UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    print ("received message:",data)