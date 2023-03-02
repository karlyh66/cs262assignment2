import socket
import time
import threading
from datetime import datetime
import random
from queue import Queue

class Client(object):
    def __init__(self, port):
        self.host = socket.gethostname()
        self.port = port
        self.rate = random.randint(1, 6)
        self.messages = Queue()
        self.logical_clock = 0
        self.incoming_clock = 0
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.connect((self.host, self.port))  # connect to the server
        print("Connected to the server!")

        # open and start writing into a log file
        self.f = open("log{}.txt".format(self.client_socket.fileno()), "w")
        self.f.write("New log started at time " + str(time.monotonic_ns()) + "\n")


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


if __name__ == "__main__":
    while True:
        port_num = input("Port? ")
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass
    Client(port_num).run()