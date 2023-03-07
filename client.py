import socket
import time
import threading
from datetime import datetime
import random
from queue import Queue
import sys
import signal
import pandas as pd

def update_logical_clock(curr_clock_val, received_val):
    return max(curr_clock_val, received_val) + 1

class Client(object):
    def __init__(self, port, id, run_no):
        self.host = socket.gethostname()
        self.port = port
        self.id = id
        self.run_no = run_no
        self.df = pd.DataFrame(columns=['event_type', 'system_time', 'old_clock_time', 'new_clock_time', 'message_queue_length'])
        self.rate = random.randint(1, 6)
        self.messages = Queue()
        self.logical_clock = 0
        self.incoming_clock = 0
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.connect((self.host, self.port))  # connect to the server
        print("Connected to the server!")
        print("Rate: " + str(self.rate))

        # open and start writing into a log file
        self.f = open("log{}_{}.txt".format(str(self.id), str(self.run_no)), "w")
        self.f.write("New log started at system time " + str(time.monotonic_ns()) + "\n")
        self.f.write("Clock rate: " + str(self.rate) + "\n")

    def signal_handler(self, sig, frame):
        print('You pressed Ctrl+C!')
        exit_message = "exit"
        self.client_socket.send(exit_message.encode())
        self.client_socket.close()
        self.df.to_csv("machine{}_{}.csv".format(str(self.id), str(self.run_no)))
        sys.exit(0)

    def listen(self):
        # handle client receiving a new message from server:
        # client puts new message into the queue
        data = self.client_socket.recv(2048) # receive the first response
        while True:
            if data.decode() == "exit":
                # when another machine exits, this one should too
                self.client_socket.close()
                self.df.to_csv("machine{}_{}.csv".format(str(self.id), str(self.run_no)))
                return
            print('Logical clock time received from server: ' + data.decode())  # show in terminal
            # self.f.write(data.decode() + "\n")
            self.messages.put(data)
            # wait to receive next response
            data = self.client_socket.recv(2048)

    def clock_cycle(self):
        time.sleep(1 / self.rate)
        # log that the client took a message off the queue
        # handle updating the logical clock time
        curr_time = str(time.monotonic_ns())

        new_row = {
            'event_type': '',
            'system_time': int(curr_time),
            'old_clock_time': self.logical_clock,
            'new_clock_time': self.logical_clock,
            'message_queue_length': 0
        }

        if not self.messages.empty():
            item = self.messages.get()
            self.logical_clock = update_logical_clock(self.logical_clock, int(item.decode()))
            print('Updated logical clock value to be ' + str(self.logical_clock))
            self.f.write('Received a message that the logical clock time is ' + item.decode() + ". New logical clock time is " + str(self.logical_clock) + ". System time is " + curr_time + ". Length of message queue: " + str(self.messages.qsize()) + ".\n")
            new_row['event_type'] = 'receive'
            new_row['message_queue_length'] = self.messages.qsize()
            new_row['new_clock_time'] = self.logical_clock
            self.df.loc[len(self.df.index)] = new_row
            return

        random_num = random.randint(1, 10)
        self.logical_clock = update_logical_clock(self.logical_clock, 0)

        # handle telling server who to send message to
        # and sending the message itself to server
        if (random_num == 1):
            total_message = "1 " + str(self.logical_clock)
            self.client_socket.send(total_message.encode())
            self.f.write("Sent to machine 1 that the logical clock time is " \
                + str(self.logical_clock) + ". The system time is " + curr_time + ".\n")
            new_row['event_type'] = 'send1'

        elif (random_num == 2):
            total_message = "2 " + str(self.logical_clock)
            self.client_socket.send(total_message.encode())
            self.f.write("Sent to machine 2 that the logical clock time is " \
                + str(self.logical_clock) + ". The system time is " + curr_time + ".\n")
            new_row['event_type'] = 'send2'

        elif (random_num == 3):
            total_message = "3 " + str(self.logical_clock)
            self.client_socket.send(total_message.encode())
            self.f.write("Sent to both machines that the logical clock time is " \
                + str(self.logical_clock) + ". The system time is " + curr_time + ".\n")
            new_row['event_type'] = 'sendboth'
            
        else:
            self.f.write("Internal event at system time " + curr_time + " and logical clock time " \
                + str(self.logical_clock) + ".\n")
            new_row['event_type'] = 'internal'
        
        new_row['new_clock_time'] = self.logical_clock
        self.df.loc[len(self.df.index)] = new_row


    def run(self):
        # start a listen thread
        data = self.client_socket.recv(2048)
        if data.decode() != "START":
            print('Bad start.')
            exit_message = "exit"
            self.client_socket.send(exit_message.encode())
            self.client_socket.close()

        listener_thread = threading.Thread(target = self.listen, args = ())
        listener_thread.start()
        signal.signal(signal.SIGINT, self.signal_handler)

        # replace this with clock_cycle() function calls (x times/sec)
        # message = input(" >> ")
        # curr_time = time.time()
        while True:
            # 1/self.rate seconds go by between each step / "action" in the process
            # right now, the action is very arbitrarily just sending the current time to all the other processes
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
    if len(sys.argv) != 2 or sys.argv[1] not in ['1', '2', '3']:
        print("Usage: client ID")
        sys.exit(1)
    port = 2000
    run_no = 4
    Client(port, int(sys.argv[1]), run_no).run()