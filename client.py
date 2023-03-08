import socket
import time
import threading
from datetime import datetime
import random
from queue import Queue
import sys
import signal
import pandas as pd

# 
def update_logical_clock(curr_clock_val, received_val):
    # handles updating the machine's logical clock
    """
        :param curr_clock_val: int, default=0: the client's current logical clock value
        :param received_val: int, default=0; if client is receiving a new message, the clock value on that message
        :return: (int) updated logical clock time
    """
    return max(curr_clock_val, received_val) + 1

class Client(object):
    def __init__(self, port, id, run_no):
        self.host = socket.gethostname()
        self.port = port
        # id and run_no are used for log.txt and .csv file naming purposes
        # hard-coded into cmd line args and main function
        self.id = id
        self.run_no = run_no
        # dataframe for organized data analysis; see report.md for details:
        # https://github.com/karlyh66/cs262assignment2/blob/main/report.md
        self.df = pd.DataFrame(columns=['event_type', 'system_time', 'old_clock_time', 'new_clock_time', 'message_queue_length'])
        self.rate = random.randint(1, 6)  # clock rate: number of ticks per minute
        # holds queued messages the that the other two machines send to this one
        self.messages = Queue()
        self.logical_clock = 0
        # socket for machine to listen to the other two server-connected machines through communicating with the server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # reuse addresses even after previous socket connection closes
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.connect((self.host, self.port))  # connect to the server

        # log to terminal
        print("Connected to the server!")
        print("Rate: " + str(self.rate))

        # open and start writing into a log file
        self.f = open("data/{}_log{}.txt".format(str(self.run_no), str(self.id)), "w")
        self.f.write("New log started at system time " + str(time.monotonic_ns()) + "\n")
        self.f.write("Clock rate: " + str(self.rate) + "\n")

    def signal_handler(self, sig, frame):
        # handle client exiting
        '''
        :param sig: the signal identification number
        :param frame: the stack frame
        :return: none
        '''
        # telling the user
        print('You pressed Ctrl+C!')
        # communicate to the two other machines to have them exit right after
        exit_message = "exit"
        self.client_socket.send(exit_message.encode())
        # machine itself exits
        self.client_socket.close()
        # collect data at the end — right before this machine terminates
        self.df.to_csv("data/{}_machine{}.csv".format(str(self.run_no), str(self.id)))
        # terminate all threads
        sys.exit(0)

    def listen(self):
        # handle machine receiving a new message from server
        data = self.client_socket.recv(2048) # receive the first response
        while True:
            if data.decode() == "exit":
                # when another machine exits, this one should too
                self.client_socket.close()
                # collect data at the end — right before this machine terminates
                self.df.to_csv("data/{}_machine{}.csv".format(str(self.run_no), str(self.id)))
                return
            print('Logical clock time received from server: ' + data.decode())  # show in terminal
            # put new message into queue
            self.messages.put(data)
            # wait to receive next response
            data = self.client_socket.recv(2048)

    def clock_cycle(self):
        # handle a clock tick
        # simulate the clock running at self.rate by having it only tick every 1 / self.rate seconds
        time.sleep(1 / self.rate)

        curr_time = str(time.monotonic_ns())

        # new entry to be placed into the data frame
        new_row = {
            'event_type': '',
            'system_time': int(curr_time),
            'old_clock_time': self.logical_clock,
            'new_clock_time': self.logical_clock,
            'message_queue_length': 0
        }

        if not self.messages.empty():
            # handle receiving a message, i.e. taking it off the queue
            item = self.messages.get()
            self.logical_clock = update_logical_clock(self.logical_clock, int(item.decode()))
            print('Updated logical clock value to be ' + str(self.logical_clock))
            self.f.write('Received a message that the logical clock time is ' + item.decode() + ". New logical clock time is " + str(self.logical_clock) + ". System time is " + curr_time + ". Length of message queue: " + str(self.messages.qsize()) + ".\n")
            new_row['event_type'] = 'receive'
            new_row['message_queue_length'] = self.messages.qsize()
            new_row['new_clock_time'] = self.logical_clock
            # add this data entry as a new row to the data frame
            self.df.loc[len(self.df.index)] = new_row
            return

        # random_num dicatates the event/action (if not receive)
        random_num = random.randint(1, 10)
        # self.logical_clock += 1
        self.logical_clock = update_logical_clock(self.logical_clock, 0)

        '''
        handle telling server who to send message to, and sending that message to server

        message format: '<recipient code> <logical clock value>'

        recipient code "1" means send to the first other machine,
        recipient code "2" means send to the second other machine,
        and recipient code "3" means send to both other machines
        '''
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
        # add this data entry as a new row to the data frame
        self.df.loc[len(self.df.index)] = new_row


    def run(self):
        # start a listener thread to add incoming messages to queue
        data = self.client_socket.recv(2048)
        # only start listener and sender threads after all three machines have connected 
        # (which the server will let this machine know about through sending the "START" string)
        if data.decode() != "START":
            print('Bad start.')
            exit_message = "exit"
            self.client_socket.send(exit_message.encode())
            self.client_socket.close()

        listener_thread = threading.Thread(target = self.listen, args = ())
        listener_thread.start()
        signal.signal(signal.SIGINT, self.signal_handler)

        # main thread == receiver + event handler + logical clock updating thread
        while True:
            self.clock_cycle()

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ['1', '2', '3']:
        print("Usage: client ID")
        sys.exit(1)
    port = 2000
    # manually updated on each new run to identify data files with that run
    run_no = 2
    Client(port, int(sys.argv[1]), run_no).run()