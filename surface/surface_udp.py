import socket
import time

#Define the array to be transferred
OUTPUT_ARRAY_WIDTH = 2
OUTPUT_ARRAY_HEIGHT = 10
output_array = [[0 for x in range(OUTPUT_ARRAY_WIDTH)] for y in range(OUTPUT_ARRAY_HEIGHT)]

#Allocate slots for each output ( in format output_array[thing][value] )
#Thrusters have first 6 positions
output_array[0][0]="Synchronisation" #Top value remains the same at all times just in case things become unsynchronised
output_array[1][0]="ForeTopThruster1"
output_array[2][0]="ForeTopThruster2"
output_array[3][0]="ForeLeftThruster"
output_array[4][0]="ForeRightThruster"
output_array[5][0]="AftLeftThruster"
output_array[6][0]="AftRightThruster"
output_array[7][0]="CameraX"
output_array[8][0]="CameraY"
output_array[9][0]="ForeLamp" #LED for illuminating surroundings

output_array[0][1]=11111 #Synchronisation value is 5 1s

#Define the array to be received
INPUT_ARRAY_WIDTH = 2
INPUT_ARRAY_HEIGHT = 1
input_array = [[0 for x in range(INPUT_ARRAY_WIDTH)] for y in range(INPUT_ARRAY_HEIGHT)]

#Allocate slots for each input ( in format input_array[thing][value] )
input_array[0][0]="Synchronisation" #Top value remains the same at all times just in case things become unsynchronised


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

#Send basic output array data
sock.sendto(bytes(str(OUTPUT_ARRAY_HEIGHT), "utf-8"), (UDP_IP, UDP_PORT))
for i in range(0, OUTPUT_ARRAY_HEIGHT):
    current_value = output_array[i][0]
    sock.sendto(bytes(str(current_value), "utf-8"), (UDP_IP, UDP_PORT))
    print("Sent data: " + str(output_array[i][0]))

#Send basic input array data
sock.sendto(bytes(str(INPUT_ARRAY_HEIGHT), "utf-8"), (UDP_IP, UDP_PORT))
for i in range(0, INPUT_ARRAY_HEIGHT):
    current_value = input_array[i][0]
    sock.sendto(bytes(str(current_value), "utf-8"), (UDP_IP, UDP_PORT))
    print("Sent data: " + str(input_array[i][0]))

while True:
    #time.sleep(0.1) #Give the pi some time to think
    print(count)
    count=count+1
    output_array[1][1]=count #Increment thruster 1 value for testing
    for i in range(0, OUTPUT_ARRAY_HEIGHT):
        current_value=output_array[i][1]
        sock.sendto(bytes(str(current_value), "utf-8"), (UDP_IP, UDP_PORT))
        print("Sent data: "+str(output_array[i][0])+" value: "+str(output_array[i][1]))

    #Test to turn LED on and off
    time.sleep(1)
    if(output_array[9][1]==0):
        output_array[9][1] = 1
    else:
        output_array[9][1] = 0