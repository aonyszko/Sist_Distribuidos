from asyncio import SendfileNotAvailableError
from time import sleep
import socket 
from threading import Thread
from random import randrange

#VARIÁVEIS GLOBAIS
SERVIDOR = ('127.0.0.1', 8999)
PORT = randrange(9000,10000)
CICLO = ('127.0.0.1', PORT)
BUFFER = 2056
FORMAT = "UTF-8"
MORREU = "M"
NOVO = "N"

#VARIÁVEIS GLOBAIS PARA ESSA APLICAÇÃO
global totalPeople

conUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
conUDP.bind(CICLO)


#SORTEIA QUANTAS PESSOAS VÃO TER NA CICLOVIA NO COMEÇO
def startCiclo():
    global totalPeople
    totalPeople = randrange(10, 70, 3)
    inicializacao = "C " + str(totalPeople)
    conUDP.sendto(inicializacao.encode(FORMAT), SERVIDOR)


#A CADA 5 SEGUNDOS 20% DE CHANCE DE UMA PESSOA IR EMBORA
def mataPessoa():
    global totalPeople
    while True:
        sleep(1)
        if(randrange(1,5,1) == 1 and totalPeople > 0):
            totalPeople -= 1
            conUDP.sendto(MORREU.encode(FORMAT),SERVIDOR)

#A CADA 5 SEGUNDOS 12% DE CHANCE DE UMA PESSOA ENTRAR NA CICLOVIA POR FORA DO APP
def geraPessoa():
    
    while True:
        sleep(1)
        if(randrange(1,8,1) == 1):
            global totalPeople
            totalPeople += 1
            conUDP.sendto(NOVO.encode(FORMAT),SERVIDOR)


#THREAD DE CONTAGEM DE TEMPO QUE O CLIENTE FICA 
def ciclista(tempo):
    sleep(tempo)
    conUDP.sendto(MORREU.encode(FORMAT),SERVIDOR)
    

#INICIA A APLICAÇÃO
#RANDOMIZA UMA QUANTIDADE PARA INICIAR A CICLOVIA
startCiclo()


#EXECUÇÃO DE THREADS 
#INICIA A CONTAGEM PARA LANÇAR 'ENTRADAS ALEATÓRIAS'
novaPessoa = Thread(target=geraPessoa)
novaPessoa.start()

#INICIA A CONTAGEM PARA LANÇAR 'MORTES ALEATÓRIAS'
contMorte = Thread(target=mataPessoa)
contMorte.start()

#FUNÇÃO 'MAIN'
while True:
    #RECEBE DO SERVIDOR O TEMPO QUE O CLIENTE IRÁ FICAR
    mensagem, servidor = conUDP.recvfrom(BUFFER)
    mensagem = mensagem.decode(FORMAT)
    
    #INICIA A EXECUÇÃO DE NOVOS CICLISTAS
    pessoa = Thread(target=ciclista,args=[int(mensagem)])
    pessoa.start()

    