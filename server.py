import socket
import copy
import threading

class Server(object):
    def __init__(self, port):
        self.host = socket.gethostname()
        self.port = port
        self.clients = [0, 0, 0]
        self.addresses = [None, None, None]
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        # this function handles accepting new client connections and spawning them off each into a new thread
        # https://stackoverflow.com/questions/23828264/how-to-make-a-simple-multithreaded-socket-server-in-python-that-remembers-client
        self.sock.listen(2)
        while True:
            self.clients[0], self.addresses[0] = self.sock.accept()
            
            self.clients[1], self.addresses[1] = self.sock.accept()

            self.clients[2], self.addresses[2] = self.sock.accept()

            # don't start until all 3 clients connected

            print("All 3 clients connected!")

            print("Client 0 connected. Socket descriptor: " + str(self.clients[0]))
            threading.Thread(target = self.handleClient,args = (self.clients[0], self.addresses[0], 0)).start()

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
        print("Client 2 file descriptor: " + str(client2))
        size = 2048
        while True:
            try:
                data = client.recv(size)
                if data:
                    # Set the response to echo back the recieved data 
                    # response = data
                    # client1.send(response)
                    # client2.send(response)
                    print(data.decode())
                    recipient, clock_val = data.decode().split()
                    print("recipient:" + recipient)
                    print("clock val:" + clock_val)
                    if recipient == "1" or recipient == "3":
                        client1.send(clock_val.encode())
                    if recipient == "2" or recipient == "3":
                        client2.send(clock_val.encode())
                else:
                    raise error('A client disconnected')
            except:
                client.close()
                return False


if __name__ == "__main__":
    port = 6000
    Server(port).listen()