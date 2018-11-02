#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Programa cliente UDP que abre un socket a un servidor."""
import socket
import sys

try:
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    METODO = sys.argv[3]
    DIRECCION = sys.argv[4]
    EXPIRES = sys.argv[5]
except IndexError:
    sys.exit("Usage: client.py ip puerto register sip_address expires_value")

ENVIAR = METODO.upper()+' sip:'+DIRECCION+' SIP/2.0 '+'EXPIRES: '+EXPIRES

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
        my_socket.connect((SERVER, PORT))
        print('')
        print(EXPIRES)
        print("Enviando:", ENVIAR + '\n')
        my_socket.send(bytes(ENVIAR,  'utf-8') + b'\r\n')
        data = my_socket.recv(1024)
        print('Recibido -- ', data.decode('utf-8'))
        
print("Socket terminado.")
