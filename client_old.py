import random
import threading
import socket

class Machine:
    def __init__(self, id, ip, port):
        self.id = id
        self.rate = random.randint(1, 6)
        self.messages = list()
        self.logical_clock = 0
        self.host = ip
        self.port = port

        f = open("log{}.txt".format(id), "w")
        f.write("New log started")

        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #     s.bind((HOST, PORT))

    def thread_fn():
        f.write("")

    def clock_cycle():
        random_num = random.randint(1, 10)

        if (random_num == 1):
            # send current local logical clock message to machine
            other_machine = 2 # change this to be not hardcoded
            f.write("Sent logical clock time " + self.logical_clock + " to machine " \
                + other_machine + "at time " + system_time)
            # update own logical clock
        
        elif (random_num == 2):
            # send current local logical clock message to machine
            other_machine = 3 # change this to be not hardcoded
            f.write("Sent logical clock time " + self.logical_clock + " to machine " \
                + other_machine + "at time " + system_time)
            # update own logical clock

        elif (random_num == 3):
            # send current local logical clock message to machine
            f.write("Sent logical clock time " + self.logical_clock + " to both machines at time " + system_time)
            # update own logical clock
        
        else:
            # update own logical clock
            f.write("Internal event at system time " + system_time + " and logical clock value " + logical_clock)

    def shutdown():
        f.close()



