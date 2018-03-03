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


# #Set up UDP
# UDP_IP = "169.254.116.33" #This needs to be the Pi's IP
# UDP_PORT = 5005
#
# #Output UDP settings
# print ("UDP target IP:", UDP_IP)
# print ("UDP target port:", UDP_PORT)
#
# sock = socket.socket(socket.AF_INET, # Internet
#                      socket.SOCK_DGRAM) # UDP


#Set up UDP input from ROV
print("Setting up surface->Pi UDP")
UDP_RECEIVE_IP = "169.254.89.249" #The Pi's IP
UDP_RECEIVE_PORT = 5005 #The port we're using
sock_receive = socket.socket(socket.AF_INET, #internet
                     socket.SOCK_DGRAM) #UDP
sock_receive.bind((UDP_RECEIVE_IP, UDP_RECEIVE_PORT))
print("UDP receiver connected:",UDP_RECEIVE_IP," Port:",UDP_RECEIVE_PORT)

#Set up UDP output to ROV
print("Setting up Pi->surface UDP")
UDP_SEND_IP = "169.254.116.33" #This needs to be the surface IP
UDP_SEND_PORT = 5005
sock_send = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
print("UDP sender connected:",UDP_SEND_IP," Port:",UDP_SEND_PORT)






count=0

#Send basic output array data
sock_send.sendto(bytes(str(OUTPUT_ARRAY_HEIGHT), "utf-8"), (UDP_SEND_IP, UDP_SEND_PORT))
print("Init output array size:", str(OUTPUT_ARRAY_HEIGHT))
for i in range(0, OUTPUT_ARRAY_HEIGHT):
    current_value = output_array[i][0]
    sock_send.sendto(bytes(str(current_value), "utf-8"), (UDP_SEND_IP, UDP_SEND_PORT))
    print("Sent label: " + str(output_array[i][0]))

#Send basic input array data
sock_send.sendto(bytes(str(INPUT_ARRAY_HEIGHT), "utf-8"), (UDP_SEND_IP, UDP_SEND_PORT))
print("Init input array size:", str(INPUT_ARRAY_HEIGHT))
for i in range(0, INPUT_ARRAY_HEIGHT):
    current_value = input_array[i][0]
    sock_send.sendto(bytes(str(current_value), "utf-8"), (UDP_SEND_IP, UDP_SEND_PORT))
    print("Sent label: " + str(input_array[i][0]))

while True:
    #time.sleep(0.1) #Give the pi some time to think
    print(count)
    count=count+1
    output_array[1][1]=count #Increment thruster 1 value for testing

    #Send output array down to ROV
    for i in range(0, OUTPUT_ARRAY_HEIGHT):
        current_value=output_array[i][1]
        sock_send.sendto(bytes(str(current_value), "utf-8"), (UDP_SEND_IP, UDP_SEND_PORT))
        print("Sent data: "+str(output_array[i][0])+" value: "+str(output_array[i][1]))

    # Get sensor data from ROV
    for i in range(0, INPUT_ARRAY_HEIGHT):
        data, addr = sock_receive.recvfrom(1024)
        input_array[i][1] = int(data.decode("utf-8"))
        print("Received data: " + str(input_array[i][0]) + " value: " + str(input_array[i][1]))


    #Test to turn LED on and off
    time.sleep(1)
    if(output_array[9][1]==0):
        output_array[9][1] = 1
    else:
        output_array[9][1] = 0