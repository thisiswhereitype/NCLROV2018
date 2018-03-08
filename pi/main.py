#This program handles the majority of the Raspberry Pi's processing for communication between the surface and ROV
#It's using separate threads for surface-Pi communication and Pi-Arduino communication
#Both threads use the global arrays for inputs and outputs

from threading import Thread
import socket
import serial
import time

#Set up serial IO for arduino
ser = serial.Serial('/dev/ttyACM0',115200)
print("Serial connected:", ser.name)

#Set up UDP input from surface
print("Setting up surface->Pi UDP")
UDP_RECEIVE_IP = "169.254.116.33" #The Pi's IP
UDP_RECEIVE_PORT = 5005 #The port we're using
sock_receive = socket.socket(socket.AF_INET, #internet
                     socket.SOCK_DGRAM) #UDP
sock_receive.bind((UDP_RECEIVE_IP, UDP_RECEIVE_PORT))
print("UDP receiver connected:",UDP_RECEIVE_IP," Port:",UDP_RECEIVE_PORT)

#Set up UDP output to surface
print("Setting up Pi->surface UDP")
UDP_SEND_IP = "169.254.89.249" #This needs to be the surface IP (Will be automatically assigned during initial code handshake)
UDP_SEND_PORT = 5005
sock_send = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
print("UDP sender connected:",UDP_SEND_IP," Port:",UDP_SEND_PORT)

# Wait for ping from surface and ping back
print ("Waiting for ping from surface.")
data, addr = sock_receive.recvfrom(1024) #Read ping
while (data.decode("utf-8")!="Ready?"):
    print("Data",str(data),"received, but not ping.")
    data, addr = sock_receive.recvfrom(1024)  # Read ping
#Get IP from surface
data, addr = sock_receive.recvfrom(1024) #Read IP
UDP_SEND_IP = data.decode("utf-8") # Save IP
print("Pring response received, new SEND_IP is",UDP_SEND_IP)
# Respond to ping and get ready for incoming data
sock_send.sendto(bytes("Ready", "utf-8"), (UDP_SEND_IP, UDP_SEND_PORT))

#Set up output array initially using received size and labels from the surface
print("Waiting for array initialisation data from surface.")
data, addr = sock_receive.recvfrom(1024) #Receive array height
OUTPUT_ARRAY_WIDTH = 2
OUTPUT_ARRAY_HEIGHT= int(data)
print("Output array is",OUTPUT_ARRAY_HEIGHT,"rows tall")
output_array = [[0 for x in range(OUTPUT_ARRAY_WIDTH)] for y in range(OUTPUT_ARRAY_HEIGHT)] #define output array
for i in range(OUTPUT_ARRAY_HEIGHT): #Fill array with string values relating to what each incoming value represents
    data, addr = sock_receive.recvfrom(1024)
    output_array[i][0] = data.decode("utf-8")
    print("Label",str(i),":",output_array[i][0])

#Set up input array initially using received size and labels from the surface
data, addr = sock_receive.recvfrom(1024) #Receive array height
INPUT_ARRAY_WIDTH = 2
INPUT_ARRAY_HEIGHT= int(data)
print("Input array is",INPUT_ARRAY_HEIGHT,"rows tall")
input_array = [[0 for x in range(INPUT_ARRAY_WIDTH)] for y in range(INPUT_ARRAY_HEIGHT)] #define input array
for i in range(INPUT_ARRAY_HEIGHT): #Fill array with string values relating to what each incoming value represents
    data, addr = sock_receive.recvfrom(1024)
    input_array[i][0] = data.decode("utf-8")
    print("Label",str(i),":",input_array[i][0])

#Reading and writing data to/from the surface via UDP
def surface_comm(thread_name):
    global output_array #Allow writing to output_array
    while True:
        #Read surface data
        i = 0
        while i < OUTPUT_ARRAY_HEIGHT:
            data, addr = sock_receive.recvfrom(1024)
            if ((data.decode("utf-8") == "11111" and i != 0)or (data.decode("utf-8") != "11111" and i == 0)):
                # If value 11111 found anywhere other than position 0, or position 0 is not 11111, then reset to position 0
                # This is to avoid writing incorrect values if there are sync issues which would cause erratic behaviour of the ROV
                print("Data sync error from surface at position",i,". Current position reset to 0.")
                i = 0

            if(data.decode("utf-8") == "Ready?"):
                #If incoming value is the initial ping which suggests the surface code was restarted
                # Respond to ping and get ready for incoming data
                print("==========Surface restart detected. Getting ready to receive data.==========")
                sock_send.sendto(bytes("Ready", "utf-8"), (UDP_SEND_IP, UDP_SEND_PORT))
                i=0
                
            else:
                output_array[i][1] = data.decode("utf-8")  # Update current value in the input array
                #print((output_array[i][0]), ":", output_array[i][1]) #DEBUG: output received value
                i += 1  # Increment i
        #Send ROV sensor data back to surface
        for i in range(0, INPUT_ARRAY_HEIGHT):
            sock_send.sendto(bytes(str(input_array[i][1]), "utf-8"), (UDP_SEND_IP, UDP_SEND_PORT))

#Reading and writing data to/from the Arduino via USB
def arduino_comm_a(thread_name):
    global output_array #Allow writing to output_array
    while True:
        #Send surface data to arduino
        i = 0
        while i < OUTPUT_ARRAY_HEIGHT:
            # Send to arduino
            ser.write((output_array[i][1] + "\n").encode("utf-8"))
            i += 1  # Increment i
            time.sleep(0.01)
            
        #Get arduino sensor data
        i = 0
        while i < INPUT_ARRAY_HEIGHT:
            # get current value
            input_array[i][1]=(ser.readline().decode("utf-8")).rstrip()
            if ((int(input_array[i][1]) == 11111 and i != 0)or (int(input_array[i][1]) != 11111 and i == 0)):
                # If value 11111 found anywhere other than position 0, or position 0 is not 11111, then reset to position 0
                # This is to avoid writing incorrect values if there are sync issues which would cause erratic behaviour of the ROV
                print("Data sync error from arduino at position",i,". Current position reset to 0.")
                i = 0
            #print(">>>>>>>>>Writing",input_array[i][1],"to position",i) #For debugging
            i += 1  # Increment i
            

def print_to_console(thread_name):
    while True:
        time.sleep(1)
        print("===RECIEVED SURFACE DATA:===")
        for i in range(OUTPUT_ARRAY_HEIGHT):
            print(i,(output_array[i][0]), ":", output_array[i][1])
        print("===RECIEVED ARDUINO DATA:===")
        for i in range(INPUT_ARRAY_HEIGHT):
            print(i,(input_array[i][0]), ":", input_array[i][1])

#Define and start threads
surface_comm = Thread( target=surface_comm, args=("Thread-1", ) )
arduino_comm_a = Thread( target=arduino_comm_a, args=("Thread-2", ) )
print_to_console = Thread( target=print_to_console, args=("Thread-3", ) )
surface_comm.start()
arduino_comm_a.start()
print_to_console.start()