import socket
import threading

class Server(object):
    def __init__(self, port):
        self.host = socket.gethostname()
        self.port = port
        # store all three client (machine) sockets
        self.clients = [0, 0, 0]
        # store all three machine addresses (as returned by socket connect function)
        self.addresses = [None, None, None]
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        # handle accepting new client connections and spawning them off each into a new thread
        self.sock.listen(2)
        while True:
            self.clients[0], self.addresses[0] = self.sock.accept()
            print("Client 0 connected. Socket descriptor: " + str(self.clients[0]))
            
            self.clients[1], self.addresses[1] = self.sock.accept()
            print("Client 1 connected. Socket descriptor: " + str(self.clients[1]))

            self.clients[2], self.addresses[2] = self.sock.accept()
            print("Client 2 connected. Socket descriptor: " + str(self.clients[2]))

            # don't start accepting messages until all 3 clients connected!
            print("All 3 clients connected!")

            # only now does server allow machines to start sending messages and ticking their clocks 
            # (the machines are blocking before this)
            start_message = "START"

            # one thread per client to listen from and send to that machine
            self.clients[0].send(start_message.encode())
            threading.Thread(target = self.handleClient,args = (self.clients[0], self.addresses[0], 0)).start()

            self.clients[1].send(start_message.encode())
            threading.Thread(target = self.handleClient,args = (self.clients[1], self.addresses[1], 1)).start()
            
            self.clients[2].send(start_message.encode())
            threading.Thread(target = self.handleClient,args = (self.clients[2], self.addresses[2], 2)).start()
    
    def handleClient(self, client, address, idx):
        # handle receiving machine messages then sending them to the correct receipients
        remaining_clients = [self.clients[i] for i in range(3) if i != idx]

        # for sending to "one of the other machines" (random number 1)
        client1 = remaining_clients[0]
        print("Client 1 file descriptor: " + str(client1)) # for debugging and monitoring

        # for sending to "the other virtual machine" (random number 2)
        client2 = remaining_clients[1]
        print("Client 2 file descriptor: " + str(client2)) # for debugging and monitoring

        size = 2048
        while True:
            data = client.recv(size)
            if data.decode() == "exit":
                    # if one machine disconnects, have the other two disconnect as well
                    print("a client disconnected")
                    exit_message = "exit"
                    client1.send(exit_message.encode())
                    client2.send(exit_message.encode())
                    return
            if data:
                # parse message received from client
                print("data: " + data.decode())
                recipient, clock_val = data.decode().split()
                print("recipient :" + recipient)
                print("clock val :" + clock_val)
                # decide which other machine (or both machines) to send to 
                if recipient == "1" or recipient == "3":
                    print("Client 1 file descriptor: " + str(client1))
                    client1.send(clock_val.encode())
                if recipient == "2" or recipient == "3":
                    print("Client 2 file descriptor: " + str(client2))
                    client2.send(clock_val.encode())

if __name__ == "__main__":
    port = 2000
    Server(port).listen()