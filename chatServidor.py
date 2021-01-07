import socket
import threading


class Server:
    def __init__(self):
        self.iniciarServidor()

    def iniciarServidor(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        host = ''
        puerto = 5555  

        self.clientes = []

        self.sock.bind((host, puerto))
        self.sock.listen(100)

        #print('Corriendo en el host: '+str(host))
        print('Corriendo en el puerto: '+str(puerto))

        self.usuarios_chat = {}

        while True:
            c, direccion = self.sock.accept()

            usuario = c.recv(1024).decode('utf-8')

            print('Nueva conexion, usuario: '+str(usuario))
            self.transmitir('Se ha unido un nuevo usuario. usuario: '+usuario)

            self.usuarios_chat[c] = usuario

            self.clientes.append(c)

            threading.Thread(target=self.clientes_chat,
                             args=(c, direccion,)).start()

    def transmitir(self, mensaje):
        for conexion in self.clientes:
            conexion.send(mensaje.encode('utf-8'))

    def clientes_chat(self, c, direccion):
        while True:
            try:
                try:
                    mensaje = c.recv(1024)
                except:
                    c.shutdown(socket.SHUT_RDWR)
                    self.clientes.remove(c)

                    print(str(self.usuarios_chat[c])+' abandono el chat.')
                    self.transmitir(
                        str(self.usuarios_chat[c])+' abandono el chat.')

                    break

                contenido = mensaje.decode('utf-8')
                if 'SALIR' in contenido:
                    c.shutdown(socket.SHUT_RDWR)
                    self.clientes.remove(c)

                    print(str(self.usuarios_chat[c])+' abandono el chat')
                    self.transmitir(
                        str(self.usuarios_chat[c])+' abandono el chat.')
                    break

                if mensaje.decode('utf-8') != '':
                    print('Nuevo mensaje: '+str(mensaje.decode('utf-8')))
                    for conexion in self.clientes:
                        if conexion != c:
                            conexion.send(mensaje)
            except:
                print('')
                self.clientes.remove(c)


server = Server()
