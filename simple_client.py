import socket
import time
import threading

class Client(object):
    def __init__(self, port):
        self.host = socket.gethostname()
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.connect((self.host, self.port))  # connect to the server
        print("Connected to the server!")

    def listen(self):
        data = self.client_socket.recv(1024) # receive response
        while data:
            print('Received from server: ' + data.decode())  # show in terminal
            data = self.client_socket.recv(1024) # receive response

    def send(self):
        # start a listen thread
        listener_thread = threading.Thread(target = self.listen, args = ())
        listener_thread.start()

        message = input(" >> ")
        while message.lower().strip() != 'exit':
            self.client_socket.send(message.encode())  # send message

            message = input(" >> ")  # again take input

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
    Client(port_num).send()