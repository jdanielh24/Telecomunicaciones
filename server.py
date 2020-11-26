#!/usr/bin/python3

# first of all import the socket library
import socket


def xor(a, b):
    resultado = []

    for i in range(1, len(b)):
        if a[i] == b[i]:
            resultado.append('0')
        else:
            resultado.append('1')

    return ''.join(resultado)



def mod2div(dividendo, divisor):
    pick = len(divisor)

    tmp = dividendo[0: pick]

    while pick < len(dividendo):

        if tmp[0] == '1':

            tmp = xor(divisor, tmp) + dividendo[pick]

        else: 
            tmp = xor('0' * pick, tmp) + dividendo[pick]

        pick += 1

    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0' * pick, tmp)

    checkword = tmp
    return checkword


def decodeData(data, key):
    l_key = len(key)

    appended_data = data + '0' * (l_key - 1)
    remainder = mod2div(appended_data, key)

    # Return the remainder
    return remainder
    '''
    print("Remainder : ", remainder)
    print("Encoded Data (Data + Remainder) : ",
          codeword)
    '''

#Creacion de socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("La creación del socket fue exitosa")

#Elegir puerto y host para servidor
puerto = 9010
host = 'localhost'

s.bind((host, puerto))
print ("socket binded to %s" % (puerto))
#Iniciar el socket para esperar datos
s.listen(5)
print ("socket esperando")


while True:
    #Establecer conexion con cliente
    c, addr = s.accept()
    print('Conexion obtenida de', addr)
    
    #obtener datos de cliente
    datos = c.recv(1024).decode('utf-8')
    
    print(datos)

    if not datos:
        break

    llave = "1001"

    ans = decodeData(datos, llave)
    print("Remainder after decoding is->"+ans)
    
    #Si en remainder todos son 0, entonces no ha ocurrido ningun error
    temp = "0" * (len(llave) - 1)
    if ans == temp:
        c.sendall(("Dato enviado ->"+datos + " Recibido sin errores FOUND").encode('utf-8'))
    else:
        c.sendall(("Error").encode('utf-8'))

    c.close()