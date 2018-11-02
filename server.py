#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Clase (y programa principal) para un servidor de eco en UDP simple."""
import sys
import json
import socketserver
import time


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """Clase principal del programa."""

    Dicc = {}

    def register2json(self):
        """Crea un archivo json."""
        """Guarda los valores de mi self.Dicc."""
        with open('registered.json', 'w') as jsonfile:
            json.dump(self.Dicc, jsonfile, indent=3)

    def json2register(self):
        """Recupera la informacion del Json creado."""
        """Carga de nuevo al ejecutar el programa."""
        try:
            with open('registered.json', 'r') as jsonfile:
                self.Dicc = json.load(jsonfile)
        except:
            pass

    def handle(self):
        """Parte principal de la clase, asigna valores a las variables."""
        """Borra los usuarios con tiempo exp = 0."""
        self.json2register()

        line = self.rfile.read()
        print("El cliente nos manda ", line.decode('utf-8'))
        ip = self.client_address[0]
        puerto = self.client_address[1]
        print("IP =", ip, "///" " Puerto =", puerto, "\n")

        linea = line.decode('utf-8')
        sip = linea.split(' ')[1]
        expires = int(linea.split(' ')[4])
        direccion = sip.split(':')[1]
        actualtime = time.strftime('%Y-%m-%d %H:%M:%S',
                                   time.gmtime(time.time()))
        exptime = time.strftime('%Y-%m-%d %H:%M:%S',
                                time.gmtime(time.time() + expires))

        while 1:
            if linea[0:8] == 'REGISTER':
                if expires != 0:
                    self.Dicc[direccion] = [ip, exptime]
                    self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                    print("SIP/2.0 200 OK\r\n\r\n")
                    print(self.Dicc)
                if expires == 0:
                    try:
                        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                        del self.Dicc[direccion]
                        print(self.Dicc)
                    except KeyError:
                        print("El diccionario esta vacio")

                self.Borrar = []

                for user in self.Dicc:
                    if actualtime >= self.Dicc[user][1]:
                        self.Borrar.append(user)
                        print(self.Borrar)

                for users in self.Borrar:
                    del self.Dicc[users]

                if not line or len(linea):
                    break
            else:
                    self.wfile.write(b"SIP/2.0 400 Bad Request\r\n")
                    print("El cliente nos manda " + "\n" + line)

        self.register2json()

if __name__ == "__main__":

    serv = socketserver.UDPServer(('', 6001), SIPRegisterHandler)

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
