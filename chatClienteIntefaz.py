import threading
import socket
import argparse
import os
import sys
import tkinter as tk


class Enviar(threading.Thread):

    def __init__(self, sock, nombre):
        super().__init__()
        self.sock = sock
        self.nombre = nombre

    def run(self):

        while True:
            print('{}: '.format(self.nombre), end='')
            sys.stdout.flush()
            mensaje = sys.stdin.readline()[:-1]

            if mensaje == 'SALIR':
                self.sock.sendall('Servidor: {} ha salido del chat.'.format(self.nombre).encode('utf-8'))
                break      
            else:
                self.sock.sendall('{}: {}'.format(self.nombre, mensaje).encode('utf-8'))
        
        print('\nSaliendo...')
        self.sock.close()
        os._exit(0)


class Recibir(threading.Thread):

    def __init__(self, sock, nombre):
        super().__init__()
        self.sock = sock
        self.nombre = nombre
        self.mensajes = None

    def run(self):
        while True:
            mensaje = self.sock.recv(1024).decode('utf-8')

            if mensaje:

                if self.mensajes:
                    self.mensajes.insert(tk.END, mensaje)
                else:
                    print('\r{}\n{}: '.format(mensaje, self.nombre), end = '')
            
            else:
                print('\nOh no!, se perdio la conexion al servidor!')
                print('\nSaliendo...')
                self.sock.close()
                os._exit(0)

class Cliente:
    def __init__(self, host, puerto):
        self.host = host
        self.puerto = puerto
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nombre = None
        self.mensajes = None
    
    def iniciar(self):

        print('Intentando conectar a {}:{}...'.format(self.host, self.puerto))
        self.sock.connect((self.host, self.puerto))
        print('Conectado exitosamente a {}:{}'.format(self.host, self.puerto))
        
        print()
        self.nombre = input('Escribe tu nombre de usuario: ')

        print()
        print('Bienvenido, {}! Preparando para enviar y recibir mensajes...'.format(self.nombre))

        env = Enviar(self.sock, self.nombre)
        rec = Recibir(self.sock, self.nombre)

        env.start()
        rec.start()

        self.sock.sendall('Servidor: {} ha entrado al chat. Di hola!'.format(self.nombre).encode('utf-8'))
        print("\rTodo listo! deja la sala escribiendo 'SALIR'\n")
        print('{}: '.format(self.nombre), end = '')

        return rec

    def send(self, entrada_texto):
 
        mensaje = entrada_texto.get()
        entrada_texto.delete(0, tk.END)
        self.mensajes.insert(tk.END, '{}: {}'.format(self.nombre, mensaje))

        if mensaje == 'SALIR':
            self.sock.sendall('Servidor: {} ha salido del chat.'.format(self.nombre).encode('utf-8'))
            
            print('\nSaliendo...')
            self.sock.close()
            os._exit(0)
        
        else:
            self.sock.sendall('{}: {}'.format(self.nombre, mensaje).encode('utf-8'))


def main():
    
    host = '96.126.114.57'
    puerto = 5555

    cliente = Cliente(host, puerto)
    recibir = cliente.iniciar()

    ventana = tk.Tk()
    ventana.title('Chat4Telecom')

    frame_mensajes = tk.Frame(master=ventana)
    scrollbar = tk.Scrollbar(master=frame_mensajes)
    mensajes_grafico = tk.Listbox(
        master=frame_mensajes, 
        yscrollcommand=scrollbar.set
    )
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
    mensajes_grafico.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    cliente.mensajes = mensajes_grafico
    recibir.mensajes = mensajes_grafico

    frame_mensajes.grid(row=0, column=0, columnspan=2, sticky="nsew")

    frame_entrada = tk.Frame(master=ventana)
    entrada_texto = tk.Entry(master=frame_entrada)
    entrada_texto.pack(fill=tk.BOTH, expand=True)
    entrada_texto.bind("<Return>", lambda x: cliente.send(entrada_texto ))
    entrada_texto.insert(0, "Mensaje...")

    btn_send = tk.Button(
        master=ventana,
        text='Enviar',
        command=lambda: cliente.send(entrada_texto)
    )

    frame_entrada.grid(row=1, column=0, padx=10, sticky="ew")
    btn_send.grid(row=1, column=1, pady=10, sticky="ew")

    ventana.rowconfigure(0, minsize=300, weight=1)
    ventana.rowconfigure(1, minsize=50, weight=0)
    ventana.columnconfigure(0, minsize=400, weight=1)
    ventana.columnconfigure(1, minsize=200, weight=0)

    ventana.mainloop()


if __name__ == '__main__':

    main()