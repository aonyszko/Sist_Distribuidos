import socket
import threading
import random

BUFFER = 2056
SERVIDOR = ('127.0.0.1', 8999)
ALIVE = True
FORMAT = "UTF-8"

while ALIVE:
    
    conUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    input("Para solicitar uma ciclovia aperte Enter")
    
    tempo = random.randrange(1000,4000,1000)
    
    conUDP.sendto(str(tempo).encode(FORMAT), SERVIDOR)
    resposta, servidor = conUDP.recvfrom(BUFFER)
    resposta = resposta.decode(FORMAT)
    print(f"Ciclovia {resposta} é a indicada")
