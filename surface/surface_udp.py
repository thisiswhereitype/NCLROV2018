import socket
import time
from threading import Thread


class ROVUDP():

    def __init__(self):
        # Define the array to be transferred
        self.OUTPUT_ARRAY_WIDTH = 2
        self.OUTPUT_ARRAY_HEIGHT = 10
        self.output_array = [[0 for x in range(self.OUTPUT_ARRAY_WIDTH)] for y in range(self.OUTPUT_ARRAY_HEIGHT)]

        # Define the array to be received
        self.INPUT_ARRAY_WIDTH = 2
        self.INPUT_ARRAY_HEIGHT = 1
        self.input_array = [[0 for x in range(self.INPUT_ARRAY_WIDTH)] for y in range(self.INPUT_ARRAY_HEIGHT)]

        #self.UDP_RECEIVE_IP = "169.254.89.249"  # This needs to be the surface IP
        self.UDP_RECEIVE_IP = socket.gethostbyname(socket.gethostname())  # Automatically retrieved surface IP
        self.UDP_RECEIVE_PORT = 5005  # The port we're using

        self.UDP_SEND_IP = "169.254.116.33"  # The Pi's IP
        self.UDP_SEND_PORT = 5005

        # Allocate slots for each output ( in format output_array[thing][1]= value )
        # Thrusters have first 6 positions
        self.output_array[0][
            0] = "Synchronisation"  # Top value remains the same at all times just in case things become unsynchronised
        self.output_array[1][0] = "ForeTopThruster1"
        self.output_array[2][0] = "ForeTopThruster2"
        self.output_array[3][0] = "ForeLeftThruster"
        self.output_array[4][0] = "ForeRightThruster"
        self.output_array[5][0] = "AftLeftThruster"
        self.output_array[6][0] = "AftRightThruster"
        self.output_array[7][0] = "CameraX"
        self.output_array[8][0] = "CameraY"
        self.output_array[9][0] = "ForeLamp"  # LED for illuminating surroundings

        self.output_array[0][1] = 11111  # Synchronisation value is 5 1s

        # Allocate slots for each input ( in format input_array[thing][value] )
        self.input_array[0][
            0] = "Synchronisation"  # Top value remains the same at all times just in case things become unsynchronised

    def connect(self):
        # Set up UDP output to ROV
        print("Setting up Surface->Pi UDP")
        self.sock_send = socket.socket(socket.AF_INET,  # Internet
                                       socket.SOCK_DGRAM)  # UDP
        print("UDP sender connected:", self.UDP_SEND_IP, " Port:", self.UDP_SEND_PORT)


        # Set up UDP input from ROV
        print("Setting up Pi->Surface UDP")
        self.sock_receive = socket.socket(socket.AF_INET,  # internet
                                          socket.SOCK_DGRAM)  # UDP
        self.sock_receive.bind((self.UDP_RECEIVE_IP, self.UDP_RECEIVE_PORT))
        print("UDP receiver connected:", self.UDP_RECEIVE_IP, " Port:", self.UDP_RECEIVE_PORT)

        # Ping Pi software to ensure it's running and everything is fine
        self.sock_send.sendto(bytes("Ready?", "utf-8"), (self.UDP_SEND_IP, self.UDP_SEND_PORT))
        self.sock_send.sendto(bytes(self.UDP_RECEIVE_IP, "utf-8"), (self.UDP_SEND_IP, self.UDP_SEND_PORT)) #Send surface IP so Pi knows where to send data (to avoid needing to set a static ip on the surface computer)
        print("Waiting for response from ROV.")
        data, addr = self.sock_receive.recvfrom(1024)    # Read ping (or any data at all which would indicate that the Pi is online)
        # If the surface has previously sent data then the pi would continue spitting out sensor data despite the surface restarting
        # Therefore any data at all is fine for this check
        print("Response received")

        # Send basic output array data
        self.sock_send.sendto(bytes(str(self.OUTPUT_ARRAY_HEIGHT), "utf-8"), (self.UDP_SEND_IP, self.UDP_SEND_PORT))
        print("Init output array size:", str(self.OUTPUT_ARRAY_HEIGHT))
        for i in range(0, self.OUTPUT_ARRAY_HEIGHT):
            current_value = self.output_array[i][0]
            self.sock_send.sendto(bytes(str(current_value), "utf-8"), (self.UDP_SEND_IP, self.UDP_SEND_PORT))
            print("Sent label: " + str(self.output_array[i][0]))

        # Send basic input array data
        self.sock_send.sendto(bytes(str(self.INPUT_ARRAY_HEIGHT), "utf-8"), (self.UDP_SEND_IP, self.UDP_SEND_PORT))
        print("Init input array size:", str(self.INPUT_ARRAY_HEIGHT))
        for i in range(0, self.INPUT_ARRAY_HEIGHT):
            current_value = self.input_array[i][0]
            self.sock_send.sendto(bytes(str(current_value), "utf-8"), (self.UDP_SEND_IP, self.UDP_SEND_PORT))
            print("Sent label: " + str(self.input_array[i][0]))

    def begin(self):
        print("==Starting UDP communication stream==")
        # Create and start threads
        rov_comm = Thread(target=self.rov_comm, args=("Thread-1",))
        rov_comm.start()

    def begin_console_output(self):
        print_to_console = Thread(target=self.print_to_console, args=("Thread-2",))
        print_to_console.start()

    def rov_comm(self, thread_name):  # All further communication with the ROV is handled in this function
        while True:
            # Send output array down to ROV
            for i in range(0, self.OUTPUT_ARRAY_HEIGHT):
                current_value = self.output_array[i][1]
                self.sock_send.sendto(bytes(str(current_value), "utf-8"), (self.UDP_SEND_IP, self.UDP_SEND_PORT))

            # Get sensor data from ROV
            i = 0
            while i < self.INPUT_ARRAY_HEIGHT:
                data, addr = self.sock_receive.recvfrom(1024)
                if ((data.decode("utf-8") == "11111" and i != 0) or (data.decode("utf-8") != "11111" and i == 0)):
                    # If value 11111 found anywhere other than position 0, or position 0 is not 11111, then reset to position 0
                    # This is to avoid writing incorrect values if there are sync issues which would cause erratic behaviour of the ROV
                    print("Data sync error from ROV at position", i, ". Current position reset to 0.")
                    i = 0
                self.input_array[i][1] = int(data.decode("utf-8"))
                i += 1  # Increment i

    def print_to_console(self, thread_name):
        while True:
            time.sleep(1)
            print("===SENT DATA:===")
            for i in range(self.OUTPUT_ARRAY_HEIGHT):
                print(i, (self.output_array[i][0]), ":", self.output_array[i][1])
            print("===RECIEVED DATA:===")
            for i in range(self.INPUT_ARRAY_HEIGHT):
                print(i, (self.input_array[i][0]), ":", self.input_array[i][1])


#Example for running code - I'm not sure exactly how to integrate this with other completed sections
udp = ROVUDP()
udp.connect()
udp.begin()
udp.begin_console_output() # For debugging only
udp.output_array[1][1] = 5;

# while True:
#     #Test to turn LED on and off
#     time.sleep(1)
#     if(output_array[9][1]==0):
#         output_array[9][1] = 1
#     else:
#         output_array[9][1] = 0
