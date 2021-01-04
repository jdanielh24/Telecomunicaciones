#!/usr/bin/python


from time import gmtime, strftime
import socket
import struct
import _thread
server = ('', 5555)
QUIT=b'adios'

class Chat:
    def __init__(self, sock, peer):
        self.sock = sock
        self.peer = peer

        _thread.start_new_thread(self.sending, ())
        self.receiving()

    def sending(self):
        while 1:
            msg = input().encode()
            tiempo = strftime("%d %b %Y %H:%M:%S: ", gmtime())
            
            cadena = struct.pack('>22s', bytes(tiempo, 'utf-8')) +msg

            self.sock.sendto(cadena, self.peer)

            if msg == QUIT :
                break

    def receiving(self) :
        while 1:
            msg, peer = self.sock.recvfrom(1024)

            print(msg.decode())

            if msg == QUIT :
                self.sock.sendto(QUIT, self.peer)
                break

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server)
    msg, client = sock.recvfrom(0, socket.MSG_PEEK)
    Chat(sock, client)