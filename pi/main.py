import socket
import serial
import time

#Set up serial output for arduino
ser = serial.Serial('/dev/ttyACM0',115200)
print("Serial connected:", ser.name)

UDP_IP = "169.254.116.33" #The Pi's IP
UDP_PORT = 5005 #The port we're using

#Set up UDP
sock = socket.socket(socket.AF_INET, #internet
                     socket.SOCK_DGRAM) #UDP
sock.bind((UDP_IP, UDP_PORT))
print("UDP connected:",UDP_IP," Port:",UDP_PORT)

#Set up array initially
print("Waiting for array initialisation data from surface.")
data, addr = sock.recvfrom(1024) #Receive array height
ARRAYWIDTH = 2
ARRAYHEIGHT= int(data)
print("Array is",ARRAYHEIGHT,"rows tall")
inputArray = [[0 for x in range(ARRAYWIDTH)] for y in range(ARRAYHEIGHT)] #define input array
for i in range(ARRAYHEIGHT): #Fill array with string values relating to what each incoming value represents
    data, addr = sock.recvfrom(1024)
    inputArray[i][0] = data.decode("utf-8")


while True:
    #Print out received values and record them in the array
    print("===RECIEVED SURFACE DATA:===")
    for i in range(ARRAYHEIGHT):
        data, addr = sock.recvfrom(1024)
        inputArray[i][1] = data.decode("utf-8") #Update current value
        print ((inputArray[i][0]),":",inputArray[i][1])
    for i in range(ARRAYHEIGHT):
        #Send to arduino
        ser.write(inputArray[i][1].encode("utf-8"))
        print("Arduino response:",ser.readline().decode("utf-8"))