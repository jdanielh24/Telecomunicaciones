import threading
import socket
import argparse
import os


class Server(threading.Thread):

    def __init__(self, host, puerto):
        super().__init__()
        self.conexiones = []
        self.host = host
        self.puerto = puerto

    def run(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.puerto))

        sock.listen(1)
        print('Escuchando:', sock.getsockname())

        while True:

            sc, socknombre = sock.accept()
            print('Nueva conexion de {} a {}'.format(
                sc.getpeername(), sc.getsockname()))

            server_socket = ServerSocket(sc, socknombre, self)
            server_socket.start()

            self.conexiones.append(server_socket)
            print('Listo para recibir mensajes de:', sc.getpeername())

    def transimitir(self, mensaje, fuente):

        for conexiones in self.conexiones:

            if conexiones.socknombre != fuente:
                conexiones.send(mensaje)

    def remove_connection(self, conexion):
        
        self.conexiones.remove(conexion)


class ServerSocket(threading.Thread):

    def __init__(self, sc, socknombre, server):
        super().__init__()
        self.sc = sc
        self.socknombre = socknombre
        self.server = server

    def run(self):
 
        while True:
            try:
                mensaje = self.sc.recv(1024).decode('utf-8')
                if mensaje:
                    print('{} dice {!r}'.format(self.socknombre, mensaje))
                    self.server.transimitir(mensaje, self.socknombre)
                else:
                    print('{} a cerrado su conexion'.format(self.socknombre))
                    self.sc.close()
                    server.remove_connection(self)
                    return
            except:
                print('error cuando kike se salio')

    def send(self, mensaje):

        self.sc.sendall(mensaje.encode('utf-8'))


def exit(servidor):

    while True:
        ipt = input('')
        if ipt == 'q':
            print('Cerrando conexiones...')
            for conexiones in servidor.conexiones:
                conexiones.sc.close()
            print('Apagando servidor...')
            os._exit(0)


if __name__ == '__main__':

    servidor = Server('96.126.114.57', 5555)
    servidor.start()

    exit = threading.Thread(target=exit, args=(servidor,))
    exit.start()
