import serial
import time

ser = serial.Serial('/dev/ttyACM0',9600)
print(ser.name)
message = b'test'
while True:
	ser.write(message)
	print("Sent message: "+message.decode("utf-8"))
	print(ser.readline())