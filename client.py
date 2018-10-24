#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import socket
import sys

# Constantes. Dirección IP del servidor y contenido a enviar
SERVER =  sys.argv[1]
PORT = 6001
LINE =  sys.argv[3:]

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
frase = ''
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, PORT))
    for pal in LINE:
        frase += pal + " " 
    print("Enviando:", frase)
    my_socket.send(bytes(frase, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8'))

print("Socket terminado.")
