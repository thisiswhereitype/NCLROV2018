from threading import Thread
import time

a = 0  #global variable

def thread1(threadname):
    while True:
        time.sleep(1)
        print(a)
    #read variable "a" modify by thread 2

def thread2(threadname):
    global a
    while True:
        a += 1
        time.sleep(1)

thread1 = Thread( target=thread1, args=("Thread-1", ) )
thread2 = Thread( target=thread2, args=("Thread-2", ) )

thread1.start()
time.sleep(0.5)
thread2.start()
#thread1.join()
#thread2.join()