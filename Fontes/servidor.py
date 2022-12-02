from time import sleep
import socket 
from threading import Thread 

# VARIÁVEIS GLOBAIS
BUFFER = 2056
EUMESMO = ('127.0.0.1', 8999)
FORMAT = "UTF-8"


#VARIÁVEIS GLOBAIS EXCLUSIVAS DESSE SCRPIT
resposta = 0
ciclovias = []

#MÉTODOS E THREADS:

#AQUI BASICAMENTE SÓ PEGAMOS E 'CRIAMOS' UMA NOVA CICLOVIA
def cicloControl(porta, pessoas):
    ciclovias.append((porta, pessoas))
    

#AQUI É O CONTROLE DE QUAL A CICLOVIA IDEAL
def melhorCiclo():
    aux = ciclovias
    
    #PRA NÃO BAGUNÇAR NOSSA LISTA DE CICLOVIAS A ORDENAÇÃO FICA NESSA VARIÁVEL AUX, O SORT VAI DEIXAR A CICLOVIA COM O MENOR NÚMERO DE PESSOAS NA FRENTE
    aux = sorted(aux, key=lambda pessoa: int(pessoa[1]))
    
    #AQUI É SÓ PARA PEGAR QUAL A PORTA DA CICLOVIA DE MENOR VALOR
    result = aux[0]
    
    #ESSA FUNÇÃO EU ACHEI NA INTERNET, BASICAMENTE ELE VAI PASSAR EM QUAL INDEX DA LISTA ESTÁ O VALOR ENCONTRADO NA VARIÁVEL RESULT
    resposta = [tup[0] for tup in ciclovias].index(result[0])
    
    print(str(ciclovias) + ", indicada ao cliente ciclovia " + str(resposta))
    return resposta


#INÍCIO DA COMUNICAÇÃO EM REDE
conUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
conUDP.bind(EUMESMO)

#FUNÇÃO 'MAIN'
while True:
    mensagem, cliente = conUDP.recvfrom(BUFFER)
    mensagem = mensagem.decode(FORMAT)
    
    #SE FOR UMA CICLOVIA SE CONECTANDO NO SERVIDOR PARA DIZER QUE 'ABRIU'
    if mensagem[0] == "C":
        endIP, porta = cliente
        
        ind, pessoas = mensagem.split()
        
        ciclovia = Thread(target=cicloControl,args=[porta, pessoas])
        ciclovia.start()
        
    
    #AQUI É O CONTROLADOR DE 'MORTE' DE PESSOAS
    elif mensagem[0] == "M":
        endIP, porta = cliente

        indice = [tup[0] for tup in ciclovias].index(porta)
        qntPessoas = int(ciclovias[indice][1]) - 1
        
        print(f"Ciclovia {porta} tem menos um ciclista")
        
        ciclovias[indice] = (porta, qntPessoas)
    
    #QUANDO A CICLOVIA MANDA UMA NOVA PESSOA QUE NÃO É ORIUNDA DO APP (SERIA O SENSOR DETECTANDO NOVA ENTRADA)
    elif mensagem[0]  == "N":
        endIP, porta = cliente
        
        indice = [tup[0] for tup in ciclovias].index(porta)
        qntPessoas = int(ciclovias[indice][1]) + 1
        
        print(f"Ciclovia {porta} tem mais um ciclista")
        
        ciclovias[indice] = (porta, qntPessoas)
        
    
    #QUANDO O 'APP ENVIA UMA MENSAGEM COM O TEMPO QUE O CLIENTE IRÁ FICAR'                 
    else:
        #PEGA A MENSAGEM E CONVERTE PARA UM INTEIRO
        tempo = int(mensagem)
        
        #VERIFICA QUAL A CICLOVIA DE MENOR NÚMERO DE PESSOAS
        responder = melhorCiclo()
        
        #PEGA A PORTA DE QUAL CICLOVIA TEM O MENOR NÚMERO DE PESSOAS
        respostaCiclovia = ciclovias[responder][0]
        
        #CRIA A TUPLA PARA COLOCAR NO SENDTO E A CICLOVIA RECEBER QUANTO TEMPO O CLIENTE IRÁ FICAR
        respostaCiclovia = ('127.0.0.1', respostaCiclovia)
        
        #ENVIA PARA A CICLOVIA MAIS LIVRE O TEMPO QUE O CLIENTE IRÁ FICAR
        conUDP.sendto(str(tempo).encode(FORMAT), respostaCiclovia)
        
        #RESPONDE AO 'APP' QUAL A CICLOVIA MAIS LIVRE
        conUDP.sendto(str(responder).encode(FORMAT), cliente)
        
        