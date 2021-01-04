#!/usr/bin/python

import socket
from servidor2 import Chat, server

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Chat(sock, server)