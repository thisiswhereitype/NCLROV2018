import socket
import time

#Define the array to be transferred
ARRAYWIDTH = 2
ARRAYHEIGHT = 10
outputArray = [[0 for x in range(ARRAYWIDTH)] for y in range(ARRAYHEIGHT)]

#Allocate slots for each output ( in format outputArray[thing][value] )
#Thrusters have first 6 positions
outputArray[0][0]="Synchronisation" #Top value remains the same at all times just in case things become unsynchronised
outputArray[1][0]="ForeTopThruster1"
outputArray[2][0]="ForeTopThruster2"
outputArray[3][0]="ForeLeftThruster"
outputArray[4][0]="ForeRightThruster"
outputArray[5][0]="AftLeftThruster"
outputArray[6][0]="AftRightThruster"
outputArray[7][0]="CameraX"
outputArray[8][0]="CameraY"
outputArray[9][0]="ForeLamp" #LED for illuminating surroundings

outputArray[0][1]=11111 #Synchronisation value is 5 1s


#Set up UDP
UDP_IP = "169.254.116.33" #This needs to be the Pi's IP
UDP_PORT = 5005
MESSAGE = "Hello World (UDP success)"

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
    #time.sleep(0.1) #Give the pi some time to think
    print(count)
    count=count+1
    outputArray[1][1]=count #Increment thruster 1 value for testing
    for i in range(0, ARRAYHEIGHT):
        currentValue=outputArray[i][1]
        sock.sendto(bytes(str(currentValue), "utf-8"), (UDP_IP, UDP_PORT))
        print("Sent data: "+str(outputArray[i][0])+" value: "+str(outputArray[i][1]))

    #Test to turn LED on and off
    time.sleep(1)
    if(outputArray[9][1]==0):
        outputArray[9][1] = 1
    else:
        outputArray[9][1] = 0