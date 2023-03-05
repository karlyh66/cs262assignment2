from multiprocessing import Process
import os
import socket
from _thread import *
import threading
import time
from threading import Thread
import random
from datetime import datetime
import random
from queue import Queue

# each threaded process has its own instance of this Machine class
# each machine has its own separate client and server threads
# this class and its member functions shoudl handle the actual client/server socket connections
class Machine():
    def __init__(self, config):
        self.config = config
        self.messages = Queue()
    def run_threads(self):
        server_thread = threading.Thread(Server(self.config).run)
        server_thread.start()
        time.sleep(5)
        client_thread = threading.Thread(Client(self.config).run)
        client_thread.start()

    # def start_server(self):
    #     HOST = str(self.config[0])
    #     PORT = int(self.config[1])
    #     print("starting server | port val:", PORT)
    #     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     s.bind((HOST, PORT))
    #     s.listen()
    #     while True:
    #         conn, addr = s.accept()
    #         # SERVER = consumer = receiver = listener
    #         start_new_thread(Server(self.config, conn).run())
    # def run(self):
    #     self.config.append(os.getpid())
    #     global code
    #     #print(config)
    #     server_thread = Thread(target=self.start_server, args=(self.config,))
    #     server_thread.start()
    #     #add delay to initialize the server-side logic on all processes
    #     time.sleep(5)
    #     # extensible to multiple producers
    #     # CLIENT = producer = sender
    #     client_thread = Thread(target=Client, args=(self.config[2],))
    #     client_thread.start()
    #     while True:
    #         # random number generation that always happens "in the background"
    #         code = random.randint(1,3)

 
# client = producer = sender of messages
# client connects to BOTH of the other ports
class Client():
    def __init__(self, config):
        self.host = "127.0.0.1"
        self.port = int(config[2])
        self.rate = random.randint(1, 6)
        self.messages = Queue()
        self.logical_clock = 0
        self.incoming_clock = 0
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.client_socket.connect((self.host, self.port))  # connect to the server
        print("Client-side connection success to port val:" + str(self.port) + "\n")

        # open and start writing into a log file
        self.f = open("log{}.txt".format(self.client_socket.fileno()), "w")
        self.f.write("New log started at time " + str(time.monotonic_ns()) + "\n")


    def run(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sleepVal = 0.500
        #sema acquired
        try:
            while True:
                codeVal = str(code)
                time.sleep(sleepVal)
                s.send(codeVal.encode('ascii'))
                print("msg sent", codeVal)
        except socket.error as e:
            print ("Error connecting producer: %s" % e)
    def listen(self):
        data = self.client_socket.recv(1024) # receive the first response
        while data:
            print('Received from server: ' + data.decode())  # show in terminal
            self.f.write(data.decode() + "\n")
            self.messages.put(data)

            # wait to receive next response
            data = self.client_socket.recv(1024)
            # message = input(" >> ")  # again take input

    def clock_cycle(self):
        if not self.messages.empty():
            item = self.messages.get()
            self.f.write(item.decode() + "\n")
            return

        random_num = random.randint(1, 10)
        curr_time = str(time.monotonic_ns())

        message = str(self.logical_clock) + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        if (random_num == 1):
            other_machine = "1" # change this to be not hardcoded
            total_message = other_machine + " " + message
            self.client_socket.send(total_message.encode())
            self.f.write("Sent logical clock time " + str(self.logical_clock) + " to machine " \
                + other_machine + "at time " + curr_time + "\n")
            self.logical_clock += 1   

        elif (random_num == 2):
            other_machine = "2" # change this to be not hardcoded
            total_message = other_machine + " " + message
            self.client_socket.send(total_message.encode())
            self.f.write("Sent logical clock time " + str(self.logical_clock) + " to machine " \
                + other_machine + "at time " + curr_time + "\n")
            self.logical_clock += 1

        elif (random_num == 3):
            other_machine = "both" # change this to be not hardcoded
            total_message = other_machine + " " + message
            self.client_socket.send(total_message.encode()) # -1 signifies to server the message is for both machines
            self.f.write("Sent logical clock time " + str(self.logical_clock) + " to both machines at time " \
                + curr_time + "\n")
            self.logical_clock += 1    

        else:
            self.f.write("Internal event at system time " + curr_time + " and logical clock value " \
                + str(self.logical_clock) + "\n")
            self.logical_clock += 1

    def run(self):
        # start a listen thread
        listener_thread = threading.Thread(target = self.listen, args = ())
        listener_thread.start()

        # replace this with clock_cycle() function calls (x times/sec)
        # message = input(" >> ")
        curr_time = time.time()
        while True:
            # 1/self.rate seconds go by between each step / "action" in the process
            # right now, the action is very arbitrarily just sending the current time to all the other processes
            time.sleep(1 / self.rate)
            self.clock_cycle()
            # # self.client_socket.send(message.encode())  # send message
            # message = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            # # message = input(" >> ")  # again take input
            # self.client_socket.send(message.encode())  # send message

        # there is an error with how we exit out of this thread, since
        # there is no python equivalent for c++'s thread.detach() function
        listener_thread.detach()

        self.client_socket.close()  # close the connection


# server = listener = consumer = receives messages
class Server():
    def __init__(self, config, conn):
        self.host = "127.0.0.1"
        self.config = config
        self.conn = conn
        self.messages = Queue()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.config[0], self.config[1]))

    def listen(self):
        # this function handles accepting new client connections and spawning them off each into a new thread
        # https://stackoverflow.com/questions/23828264/how-to-make-a-simple-multithreaded-socket-server-in-python-that-remembers-client
        self.sock.listen(2)
        conn, addr = self.sock.accept()
        client_thread = threading.Thread(Client(self.config).run)
        client_thread.start()
        while True:
            conn, addr = self.sock.accept()
            threading.Thread(target = self.handleClient, args = (self.clients[0], self.addresses[0], 0)).start()

            print("Client 1 connected. Socket descriptor: " + str(self.clients[1]))
            threading.Thread(target = self.handleClient,args = (self.clients[1], self.addresses[1], 1)).start()
            
            print("Client 2 connected. Socket descriptor: " + str(self.clients[2]))
            threading.Thread(target = self.handleClient,args = (self.clients[2], self.addresses[2], 2)).start()
    
    def handleClient(self, client, address, idx):
        # handling receiving client messages then sending them to the correct receipients
        remaining_clients = [self.clients[i] for i in range(3) if i != idx]
        client1 = remaining_clients[0]
        print("Client 1 file descriptor: " + str(client1))
        client2 = remaining_clients[1]
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    # Set the response to echo back the recieved data 
                    response = data
                    if (data.decode() == "exit"):
                        print("Client with file descriptor" + client + "disconnected.")
                    client1.send(response)
                    client2.send(response)
                else:
                    raise error('A client disconnected')
            except:
                client.close()
                return False
        
 
if __name__ == '__main__':
    localHost= "127.0.0.1"
    port1 = 1024
    port2 = 2024
    port3 = 3024
    config1 = [localHost, port1, port2]
    p1 = Process(target=Machine(config1).run())
    config2 = [localHost, port2, port3]
    p2 = Process(target=Machine(config2).run())
    config3 = [localHost, port3, port1]
    p3 = Process(target=Machine(config3).run())

    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()