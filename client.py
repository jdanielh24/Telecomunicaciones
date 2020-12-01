<<<<<<< HEAD
# Importar modulo de socket
=======
>>>>>>> 4b99b739739d51f4b370a666dd168079d1cb8ecf
import socket               
 


def xor(a, b):
 
    # inicializar resultado
    resultado = []
 
    # Recorrer todos los bits, si los bits son iguales
    # entonces XOR es 0, sino 1
    for i in range(1, len(b)):
        if a[i] == b[i]:
            resultado.append('0')
        else:
            resultado.append('1')
 
    return ''.join(resultado)
 
 
# Realizar division Modulo-2 
def mod2div(divident, divisor):
    
    pick = len(divisor)
 
    tmp = divident[0 : pick]
 
    while pick < len(divident):
 
        if tmp[0] == '1':
 
            tmp = xor(divisor, tmp) + divident[pick]
 
        else:  
            tmp = xor('0'*pick, tmp) + divident[pick]
 
        pick += 1
 
    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0'*pick, tmp)
 
    checkword = tmp
    return checkword
 
def encodeData(data, key):
 
    l_key = len(key)
 
    appended_data = data + '0'*(l_key-1)
    remainder = mod2div(appended_data, key)

    codeword = data + remainder
    return codeword    
    '''
    print("Remainder : ", remainder)
    print("Encoded Data (Data + Remainder) : ",
          codeword)
    '''



# Crear objeto socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
 
# Definir la ip del servidor y el puerto al que se conectara
#host = '187.189.20.216'
host = 'localhost'
puerto = 9999           
 
# conectar con el servidor
s.connect((host, puerto))

# guardar datos de entrada del usuario
info = input("Ingresa los datos que quieres enviar->")
#s.sendall(input_string)
datos =(''.join(format(ord(x), 'b') for x in info))
print (datos)
llave = "1001"

ans = encodeData(datos,llave)
print(ans)
s.sendall(ans.encode('utf-8'))


# Recibir datos del servidor
print (s.recv(1024).decode('utf-8'))

# Cerrar la conexion
s.close()