import socket
import time

#Define the array to be transferred
ARRAYWIDTH = 2
ARRAYHEIGHT = 9
outputArray = [[0 for x in range(ARRAYWIDTH)] for y in range(ARRAYHEIGHT)]

#Allocate slots for each output ( in format outputArray[thing][value] )
#Thrusters have first 6 positions
outputArray[0][0]="ForeTopThruster1"
outputArray[1][0]="ForeTopThruster2"
outputArray[2][0]="ForeLeftThruster"
outputArray[3][0]="ForeRightThruster"
outputArray[4][0]="AftLeftThruster"
outputArray[5][0]="AftRightThruster"
outputArray[6][0]="CameraX"
outputArray[7][0]="CameraY"
outputArray[8][0]="ForeLamp" #LED for illuminating surroundings


#Set up UDP
UDP_IP = "169.254.116.33" #This needs to be the Pi's IP
UDP_PORT = 5005
MESSAGE = "Hello"

#Output UDP settings
print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)
print ("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
count=0

#Send basic array data
sock.sendto(bytes(str(ARRAYHEIGHT), "utf-8"), (UDP_IP, UDP_PORT))
for i in range(0, ARRAYHEIGHT):
    # currentItem = outputArray[i][0]
    currentValue = outputArray[i][0]
    sock.sendto(bytes(str(currentValue), "utf-8"), (UDP_IP, UDP_PORT))
    print("Sent data: " + str(outputArray[i][0]))


while True:
    time.sleep(0.1)
    print(count)
    count=count+1
    outputArray[0][1]=count
    for i in range(0, ARRAYHEIGHT):
        currentValue=outputArray[i][1]
        sock.sendto(bytes(str(currentValue), "utf-8"), (UDP_IP, UDP_PORT))
        print("Sent data: "+str(outputArray[i][0])+" value: "+str(outputArray[i][1]))