import socket
import time
import threading
from datetime import datetime
import random
from queue import Queue
import sys

class Client(object):
    def __init__(self, port, id):
        self.host = socket.gethostname()
        self.port = port
        self.id = id
        self.rate = random.randint(1, 6)
        self.messages = Queue()
        self.logical_clock = 0
        self.incoming_clock = 0
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.connect((self.host, self.port))  # connect to the server
        print("Connected to the server!")
        print("Rate: " + str(self.rate))

        # open and start writing into a log file
        self.f = open("log{}.txt".format(str(self.id)), "w")
        self.f.write("New log started at system time " + str(time.monotonic_ns()) + "\n")
        self.f.write("Clock rate: " + str(self.rate) + "\n")

    def listen(self):
        # handle client receiving a new message from server:
        # client puts new message into the queue
        data = self.client_socket.recv(1024) # receive the first response
        while data:
            # print('Logical clock time received from server is ' + data.decode())  # show in terminal
            # self.f.write(data.decode() + "\n")
            self.messages.put(data)

            # wait to receive next response
            data = self.client_socket.recv(1024)

    def clock_cycle(self):
        # change to 1 / self.rate later
        time.sleep(2 / self.rate)
        # log that the client took a message off the queue
        # handle updating the logical clock time
        curr_time = str(time.monotonic_ns())

        if not self.messages.empty():
            item = self.messages.get()
            self.logical_clock = max(self.logical_clock, int(item.decode())) + 1
            # self.logical_clock = int(item.decode()) + 1
            print('Updated logical clock value to now be ' + str(self.logical_clock))
            self.f.write('Received a message that the logical clock time is ' + item.decode() + ". New logical clock time is " + str(self.logical_clock) + ". System time is " + curr_time + ". Length of message queue: " + str(self.messages.qsize()) + ".\n")
            return

        random_num = random.randint(1, 10)

        # handle telling server who to send message to
        # and sending the message itself to server
        if (random_num == 1):
            total_message = "1 " + str(self.logical_clock)
            self.client_socket.send(total_message.encode())
            self.f.write("Sent to machine 1 that the logical clock time is " \
                + str(self.logical_clock) + ". The system time is " + curr_time + ".\n")
            self.logical_clock += 1

        elif (random_num == 2):
            total_message = "2 " + str(self.logical_clock)
            self.client_socket.send(total_message.encode())
            self.f.write("Sent to machine 2 that the logical clock time is " \
                + str(self.logical_clock) + ". The system time is " + curr_time + ".\n")
            self.logical_clock += 1

        elif (random_num == 3):
            total_message = "3 " + str(self.logical_clock)
            self.client_socket.send(total_message.encode())
            self.f.write("Sent to both machines that the logical clock time is " \
                + str(self.logical_clock) + ". The system time is " + curr_time + ".\n")
            self.logical_clock += 1

        else:
            self.f.write("Internal event at system time " + curr_time + " and logical clock time " \
                + str(self.logical_clock) + ".\n")
            self.logical_clock += 1

        print('Updated logical clock value to now be ' + str(self.logical_clock))

    def run(self):
        # start a listen thread
        listener_thread = threading.Thread(target = self.listen, args = ())
        listener_thread.start()

        while True:
            # handle everything in the clock_cycle() function
            self.clock_cycle()

        # there is an error with how we exit out of this thread, since
        # there is no python equivalent for c++'s thread.detach() function
        listener_thread.detach()

        self.client_socket.close()  # close the connection


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ['1', '2', '3']:
        print("Usage: client ID")
        sys.exit(1)
    port = 6000
    Client(port, int(sys.argv[1])).run()