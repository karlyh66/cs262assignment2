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
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        # this function handles accepting new client connections and spawning them off each into a new thread
        # https://stackoverflow.com/questions/23828264/how-to-make-a-simple-multithreaded-socket-server-in-python-that-remembers-client
        self.sock.listen(2)
        while True:
            self.clients[0], self.addresses[0] = self.sock.accept()
            print("Client 0 connected. Socket descriptor: " + str(self.clients[0]))
            threading.Thread(target = self.handleClient,args = (self.clients[0], self.addresses[0], self.clients)).start()
            self.clients[1], self.addresses[1] = self.sock.accept()
            print("Client 1 connected. Socket descriptor: " + str(self.clients[1]))
            threading.Thread(target = self.handleClient,args = (self.clients[1], self.addresses[1], self.clients)).start()
            self.clients[2], self.addresses[2] = self.sock.accept()
            print("Client 2 connected. Socket descriptor: " + str(self.clients[2]))
            threading.Thread(target = self.handleClient,args = (self.clients[2], self.addresses[2], self.clients)).start()
    
    def handleClient(self, client, address, all_clients):
        # handling receiving client messages then sending them to the correct receipients
        remaining_clients = [c for c in all_clients if c.fileno() != client.fileno()]
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
                    client.send(response)
                    client1.send(response)
                else:
                    raise error('A client disconnected')
            except:
                client.close()
                return False


if __name__ == "__main__":
    while True:
        port_num = input("Port? ")
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass
    Server(port_num).listen()