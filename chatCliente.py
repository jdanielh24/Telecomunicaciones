import socket
import threading

class Client:
    def __init__(self):
        self.crearConexion()

    def crearConexion(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        while 1:
            try:
                host = '96.126.114.57'
                port = 5555
                self.sock.connect((host,port))
                
                break
            except:
                print("No se pudo conectar con el servidor")

        self.nombre = input('Ingresa el nombre de usuario--> ')
        self.sock.send(self.nombre.encode('utf-8'))
        
        mensaje = threading.Thread(target=self.mensajes,args=())
        mensaje.start()

        entrada = threading.Thread(target=self.entrada,args=())
        entrada.start()

    def mensajes(self):
        while 1:
            print(self.sock.recv(1204).decode('utf-8'))

    def entrada(self):
        while 1:
            self.sock.send((self.nombre+' - '+input()).encode('utf-8'))

client = Client()