import socketserver
import socket
import threading
import time

SERVER_PORT = 25565

class ChatServer():
    def __init__(self, address):
        assert type(address) == tuple
        try:
            self.MasterSocket = socket.create_server(("",SERVER_PORT),family=socket.AF_INET6, dualstack_ipv6=True)
            self.Clients = dict()
        except Exception as e:
            print(e)

    def broadcast(self,data):
        for client in self.Clients.values():
            try:
                client.sendall(data)
            except Exception as e:
                print("Failed to send to client: " + repr(e))

    def client(self,conn):
        while True:
            try:
                data = conn.recv(1024)
                if not data: break

                print(data.decode())
                
                self.broadcast(data)
            except Exception as e:
                print("Something weird happened to client handler: " + repr(e))
                break

        del self.Clients[conn.getpeername()[1]]

    def serve_forever(self):
        while True:
            try:
                conn, addr = self.MasterSocket.accept()

                print(conn.getsockname()[0] + " has connected!")
                
                self.Clients[conn.getpeername()[1]] = conn
                threading.Thread(target=self.client,args=(conn,)).start()
            except Exception as e:
                print(e)

chat_server = ChatServer(("localhost", SERVER_PORT))

threading.Thread(target=chat_server.serve_forever).start()
#chat_server.serve_forever()       

"""
class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).decode()
        print(self.data)

        self.request.sendall("what's up BRO".encode())

tcp_server = socketserver.TCPServer(("localhost",SERVER_PORT),TCPHandler)

tcp_server.serve_forever()
"""

