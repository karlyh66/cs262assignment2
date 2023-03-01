import random
import threading
import time
import socket
import sys

class Machine:
    def __init__(self, id, ip, port):
        self.id = id
        self.rate = random.randint(1, 6)
        self.messages = list()
        self.logical_clock = 0
        self.HOST = ip
        self.PORT = port

        self.f = open("log{}.txt".format(id), "w")
        f.write("New log started at time " + time.monotonic_ns() + "\n")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))

            send_thread = threading.Thread(target=send_thread, args=(s))
            listen_thread = threading.Thread(target=listen_thread, args=(s))
            send_thread.start()
            listen_thread.start()

    def send_thread(s):
        continue

    def listen_thread(s):
        while True:
            data = s.recv(1024) 
            prev_logical_clock = self.logical_clock
            self.logical_clock = max(int(data), self.logical_clock) + 1
            self.f.write("Received message " + data + ", current logical clock " \
                + prev_logical_clock + " updated to " + self.logical_clock "\n")

    def clock_cycle(s):
        random_num = random.randint(1, 10)

        if (random_num == 1):
            other_machine = 2 # change this to be not hardcoded
            s.sendall(other_machine + " " + self.logical_clock)
            f.write("Sent logical clock time " + self.logical_clock + " to machine " \
                + other_machine + "at time " + time.monotonic_ns() + "\n")
            self.logical_clock += 1   

        elif (random_num == 2):
            other_machine = 3 # change this to be not hardcoded
            s.sendall(other_machine + " " + self.logical_clock)
            f.write("Sent logical clock time " + self.logical_clock + " to machine " \
                + other_machine + "at time " + time.monotonic_ns() + "\n")
            self.logical_clock += 1

        elif (random_num == 3):
            s.sendall(-1 + " " + self.logical_clock) # -1 signifies to server the message is for both machines
            f.write("Sent logical clock time " + self.logical_clock + " to both machines at time " \
                + time.monotonic_ns() + "\n")
            self.logical_clock += 1    

        else:
            f.write("Internal event at system time " + time.monotonic_ns() + " and logical clock value " \
                + logical_clock + "\n")
            self.logical_clock += 1

    def shutdown():
        f.write("Closing log at system time " + time.monotonic_ns() + "\n")
        f.close()

#=======================================================================#
#===========================* main sequence *===========================#
#=======================================================================#

if len(sys.argv != 4):
    print("Usage should be machine.py machine_id host_ip port")

args = sys.argv # usage: machine.py id ip port
machine = Machine(args[1], args[2], args[3])