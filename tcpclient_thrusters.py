import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import logging
import sys
import time
import socket
import json
from threading import Thread
#from Adafruit_BNO055 import BNO055

'''
Set Pins here
Names indicate the location of the thruster on the ROV rather than its movement
'''
port_thruster = "P9_16"
bow_thruster = "P8_13"
stern_thruster = "P9_14"
starboard_thruster = "P8_19"
armclose_thruster = "P9_21"
armrotate_thruster = "P9_22"

'''
Set Max, Min Duty Cycle here
'''
max_reverse_duty_cycle = 6.0
no_power_duty_cycle = 7.5
actual_duty_cycle = 7.5
max_forward_duty_cycle = 9.0

'''
Set selected thursters
'''

b_port_thruster = False
b_bow_thruster = False
b_stern_thruster = False
b_starboard_thruster = False
b_armclose_thruster = False
b_armrotate_thruster = False
wake_up_duration = 4

'''PWM start'''
print 'Init port thruster'
PWM.start(port_thruster,7.5,50)
time.sleep(wake_up_duration)
print 'Init starboard thruster'
PWM.start(starboard_thruster,7.5,50)
time.sleep(wake_up_duration)
print 'Init bow thruster'
PWM.start(bow_thruster,7.5,50)
time.sleep(wake_up_duration)
print 'Init stern thruster'
PWM.start(stern_thruster,7.5,50)
time.sleep(wake_up_duration)
print 'Init arm rotate thruster'
PWM.start(armclose_thruster,7.5,50)
time.sleep(wake_up_duration)
print 'Init arm close thruster'
PWM.start(armrotate_thruster,7.5,50)
time.sleep(wake_up_duration)

'''
Disabled BNO055 module as we cannot test it for now, will be introduced for 
final testing
'''
#bno = BNO055.BNO055(busnum=2, rst='P9_12')

'''
Enable verbose debug logging if -v is passed as a parameter.
'''
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)
    
'''
Initialize the BNO055 and stop if something went wrong.
'''
#if not bno.begin():
#    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

'''
Print system status and self test result.
'''
#status, self_test, error = bno.get_system_status()
#print('System status: {0}'.format(status))
#print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))

'''
Print out an error if system status is in error mode.
'''
#if status == 0x01:
#    print('System error: {0}'.format(error))
#    print('See datasheet section 4.3.59 for the meaning.')

#print('Reading BNO055 data, press Ctrl-C to quit...')

#def gyro():
#	while running:
#		heading, roll, pitch = bno.read_euler()
#		if (printGyro):
#			print("Heading: " + str(heading) + " Roll: " + str(roll) + " Pitch: " + str(pitch))
#		time.sleep(sleep)

#gyroT = Thread(target=gyro)
#gyroT.start()

#Initialize Joystick class and init an object joystick of that class with values 0
class Joystick(object):
    button_up = -1
    button_down = -1
    hat = -1
    hat_value = 0
    axis = 0
    axis_value = 0
    
    def __init__(self, j):
        self.__dict__ = json.loads(j)
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
#server_address = ('192.168.7.1', 10000)
server_address = ('169.254.246.139', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    while True:
        data = sock.recv(128)
        if len(data) > 0 :
            joystick = Joystick(data)
        else: 
            break
        
        #thruster front directional duty cycle
        if joystick.axis == 3:
            b_bow_thruster = False
            b_stern_thruster = False
            b_port_thruster = True
            b_starboard_thruster = True
            if joystick.axis_value <  0:
                joystick.axis_value = joystick.axis_value * (-1)
                range_duty_cycle = max_forward_duty_cycle - no_power_duty_cycle
                actual_duty_cycle = (range_duty_cycle * joystick.axis_value) + no_power_duty_cycle
            elif joystick.axis_value > 0:
                range_duty_cycle = no_power_duty_cycle - max_reverse_duty_cycle
                actual_duty_cycle = no_power_duty_cycle - (range_duty_cycle * joystick.axis_value)
            elif joystick.axis_value == 0:
                b_port_thruster = False
                b_starboard_thruster = False
                actual_duty_cycle = no_power_duty_cycle
        
        #thruster sideways directional duty cycle
        if joystick.axis == 4:
            b_bow_thruster = False
            b_stern_thruster = False
            if joystick.axis_value < 0:
                joystick.axis_value = joystick.axis_value * (-1)
                b_starboard_thruster = True
                range_duty_cycle = max_forward_duty_cycle - no_power_duty_cycle
                actual_duty_cycle = (range_duty_cycle * joystick.axis_value) + no_power_duty_cycle
            elif joystick.axis_value > 0:
                b_port_thruster = True
                range_duty_cycle = max_forward_duty_cycle - no_power_duty_cycle
                actual_duty_cycle = (range_duty_cycle * joystick.axis_value) + no_power_duty_cycle
            elif joystick.axis_value == 0:
                b_port_thruster = False
                b_starboard_thruster = False
                actual_duty_cycle = no_power_duty_cycle
        
        #thruster verital duty cycle
        if joystick.axis == 1:
            b_bow_thruster = True
            b_stern_thruster = True
            b_port_thruster = False
            b_starboard_thruster = False
            if joystick.axis_value < 0:
                joystick.axis_value = joystick.axis_value * (-1)
                range_duty_cycle = max_forward_duty_cycle - no_power_duty_cycle
                actual_duty_cycle = (range_duty_cycle * joystick.axis_value) + no_power_duty_cycle
            elif joystick.axis_value > 0:
                range_duty_cycle = no_power_duty_cycle - max_reverse_duty_cycle
                actual_duty_cycle = no_power_duty_cycle - (range_duty_cycle * joystick.axis_value)
            elif joystick.axis_value == 0:
                b_bow_thruster = False
                b_stern_thruster = False
                actual_duty_cycle = no_power_duty_cycle

        #thruster mechenical arm duty cycle
        if joystick.axis == 2:
            b_bow_thruster = False
            b_stern_thruster = False
            b_port_thruster = False
            b_starboard_thruster = False
            if joystick.axis_value < 0:
                range_duty_cycle = max_forward_duty_cycle - no_power_duty_cycle
                actual_duty_cycle = (range_duty_cycle * joystick.axis_value) + no_power_duty_cycle
            elif joystick.axis_value > 0:
                range_duty_cycle = no_power_duty_cycle - max_reverse_duty_cycle
                actual_duty_cycle = no_power_duty_cycle - (range_duty_cycle * joystick.axis_value)
            elif joystick.axis_value == 0:
                actual_duty_cycle = no_power_duty_cycle
            
        #close mechanical arm
        if joystick.button_up == 3:
            b_armclose_thruster = False
        if joystick.button_down == 3:
            b_armclose_thruster = True

        #rotate mechanical arm
        if joystick.button_up == 1:
            b_armrotate_thruster = False
        if joystick.button_down == 1:
            b_armrotate_thruster = True

        #power to thruster
        if b_port_thruster:
            PWM.set_duty_cycle(port_thruster, actual_duty_cycle)
        else:
            PWM.set_duty_cycle(port_thruster, no_power_duty_cycle)
            
        if b_starboard_thruster:
            PWM.set_duty_cycle(starboard_thruster, actual_duty_cycle)
        else:
            PWM.set_duty_cycle(starboard_thruster, no_power_duty_cycle)
            
        
        if b_stern_thruster:
            PWM.set_duty_cycle(stern_thruster, actual_duty_cycle)
        else:
            PWM.set_duty_cycle(stern_thruster, no_power_duty_cycle)
            
        
        if b_bow_thruster:
            PWM.set_duty_cycle(bow_thruster, actual_duty_cycle)
        else:
            PWM.set_duty_cycle(bow_thruster, no_power_duty_cycle)
            
        
        if b_armclose_thruster:
            PWM.set_duty_cycle(armclose_thruster, actual_duty_cycle)
        else:
            PWM.set_duty_cycle(armclose_thruster, no_power_duty_cycle)
            
        
        if b_armrotate_thruster:
            PWM.set_duty_cycle(armrotate_thruster, actual_duty_cycle)
        else:
            PWM.set_duty_cycle(armrotate_thruster, no_power_duty_cycle)
            
        

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
    