#This program handles the majority of the Raspberry Pi's processing for communication between the surface and ROV
#It's using separate threads for surface-Pi communication and Pi-Arduino communication
#Both threads use the global arrays for inputs and outputs (OUTPUTS NOT YET IMPLEMENTED)

from threading import Thread
import socket
import serial
import time

#Set up serial IO for arduino
ser = serial.Serial('/dev/ttyACM0',115200)
print("Serial connected:", ser.name)

#Set up UDP IO for surface
UDP_IP = "169.254.116.33" #The Pi's IP
UDP_PORT = 5005 #The port we're using
sock = socket.socket(socket.AF_INET, #internet
                     socket.SOCK_DGRAM) #UDP
sock.bind((UDP_IP, UDP_PORT))
print("UDP connected:",UDP_IP," Port:",UDP_PORT)

#Set up array initially using received size and labels from the surface
print("Waiting for array initialisation data from surface.")
data, addr = sock.recvfrom(1024) #Receive array height
OUTPUT_ARRAY_WIDTH = 2
OUTPUT_ARRAY_HEIGHT= int(data)
print("Array is",OUTPUT_ARRAY_HEIGHT,"rows tall")
output_array = [[0 for x in range(OUTPUT_ARRAY_WIDTH)] for y in range(OUTPUT_ARRAY_HEIGHT)] #define input array
for i in range(OUTPUT_ARRAY_HEIGHT): #Fill array with string values relating to what each incoming value represents
    data, addr = sock.recvfrom(1024)
    output_array[i][0] = data.decode("utf-8")

#Reading and writing data to/from the surface via UDP
def surface_comm(thread_name):
    global output_array #Allow writing to output_array
    while True:
        #Read surface data
        i = 0
        while i < OUTPUT_ARRAY_HEIGHT:
            data, addr = sock.recvfrom(1024)
            if ((data.decode("utf-8") == "11111" and i != 0)or (data.decode("utf-8") != "11111" and i == 0)):
                # If value 11111 found anywhere other than position 0, or position 0 is not 11111, then reset to position 0
                # This is to avoid writing incorrect values if there are sync issues which would cause erratic behaviour of the ROV
                print("Data sync error from surface at position",i,". Current position reset to 0.")
                i = 0
            output_array[i][1] = data.decode("utf-8")  # Update current value in the input array
            #print((output_array[i][0]), ":", output_array[i][1]) #DEBUG: output received value
            i += 1  # Increment i

#Reading and writing data to/from the Arduino via USB
def arduino_comm_a(thread_name):
    global output_array #Allow writing to output_array
    while True:
        #Read surface data
        i = 0
        while i < OUTPUT_ARRAY_HEIGHT:
            # Send to arduino
            ser.write((output_array[i][1] + "\n").encode("utf-8"))
            i += 1  # Increment i
            time.sleep(0.01)

def print_to_console(thread_name):
    while True:
        time.sleep(0.1)#Print to console every 0.1 seconds
        print("===RECIEVED SURFACE DATA:===")
        for i in range(OUTPUT_ARRAY_HEIGHT):
            print((output_array[i][0]), ":", output_array[i][1])

#Define and start threads
surface_comm = Thread( target=surface_comm, args=("Thread-1", ) )
arduino_comm_a = Thread( target=arduino_comm_a, args=("Thread-2", ) )
print_to_console = Thread( target=print_to_console, args=("Thread-3", ) )
surface_comm.start()
arduino_comm_a.start()
print_to_console.start()