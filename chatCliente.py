import socket
import threading

class Client:
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        while 1:
            try:
                host = '96.126.114.57'
                port = 5555
                self.s.connect((host,port))
                
                break
            except:
                print("Couldn't connect to server")

        self.username = input('Enter username --> ')
        self.s.send(self.username.encode('utf-8'))
        
        message_handler = threading.Thread(target=self.handle_messages,args=())
        message_handler.start()

        input_handler = threading.Thread(target=self.input_handler,args=())
        input_handler.start()

    def handle_messages(self):
        while 1:
            print(self.s.recv(1204).decode('utf-8'))

    def input_handler(self):
        while 1:
            self.s.send((self.username+' - '+input()).encode('utf-8'))

client = Client()