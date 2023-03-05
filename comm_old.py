from multiprocessing import Process
import os
import socket
from _thread import *
import threading
import time
from threading import Thread
import random
 

# client
# or whoever sends messages
def producer(portVal):
    host= "127.0.0.1"
    port = int(portVal)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sleepVal = 0.500
    #sema acquired
    try:
        s.connect((host,port))
        print("Client-side connection success to port val:" + str(portVal) + "\n")
        while True:
            codeVal = str(code)
            time.sleep(sleepVal)
            s.send(codeVal.encode('ascii'))
            print("msg sent", codeVal)
    except socket.error as e:
        print ("Error connecting producer: %s" % e)


# server
# or whoever receives messages
def consumer(conn):
    print("consumer accepted connection" + str(conn)+"\n")
    msg_queue=[]
    sleepVal = 0.900
    while True:
        time.sleep(sleepVal)
        data = conn.recv(1024)
        print("msg received\n")
        print("msg received:", dataVal)
        msg_queue.append(dataVal)
 

def init_machine(config):
    # config[0] is the localhost string
    HOST = str(config[0])
    # config[1] is the first numerical argument
    PORT = int(config[1])
    print("starting server | port val:", PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        start_new_thread(consumer, (conn,))
 

def machine(config):
    config.append(os.getpid())
    global code
    #print(config)
    # SERVER connection
    # this one starts a "consumer" thread
    init_thread = Thread(target=init_machine, args=(config,))
    init_thread.start()
    #add delay to initialize the server-side logic on all processes
    time.sleep(5)
    # extensible to multiple producers
    # CLIENT connection
    prod_thread = Thread(target=producer, args=(config[2],))
    prod_thread.start()
    while True:
        code = random.randint(1,3)
        
 
if __name__ == '__main__':
    localHost= "127.0.0.1"
    port1 = 1024
    port2 = 2024
    port3 = 3024
    config1=[localHost, port1, port2]
    p1 = Process(target=machine, args=(config1,))
    config2=[localHost, port2, port3]
    p2 = Process(target=machine, args=(config2,))
    config3=[localHost, port3, port1]
    p3 = Process(target=machine, args=(config3,))
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()