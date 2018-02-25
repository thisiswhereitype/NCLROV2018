import serial
import time

ser = serial.Serial('/dev/ttyACM0',9600)
print(ser.name)
message = b'test'
while True:
	ser.write(message)
	print("Sent message: "+message)
	time.sleep(5)
	#ser.close()