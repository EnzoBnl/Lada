import socket

from struct import pack
from struct import unpack
from struct import calcsize as sizeof


CONNECT_TO_CAR = 1
MOVE_CAR = 2
GET_MALUS = 3
SEND_MALUS = 4


# Cree un paquet avec le code du type de message
def create_packet(op_code, data):
    return pack("!I{}s".format(len(data)), op_code, data.encode())


# Extrait le code du type de message ainsi que les donnees du paquet
def process_packet(packet):
    return unpack("!I{}s".format(len(packet)-sizeof("!I")), packet)


#code client pour forwarder à la voiture
import socket
TCP_IP = '192.168.1.101'
TCP_PORT = 8890
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
def forward_voiture(MESSAGE):
    
    s.send(MESSAGE)
    data = s.recv(BUFFER_SIZE)
#fin code client voiture

TCP_IP = '192.168.1.22'
TCP_PORT = 1337
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
s2= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.bind((TCP_IP, TCP_PORT))
s2.listen(1)
conn, addr = s2.accept()
print('Connection address:', addr)
compteur = 0
while 1:
    compteur += 1
    if (compteur % 3 == 0):
        conn.send(create_packet(GET_MALUS,""))
    data = conn.recv(BUFFER_SIZE)
    print("received data:", process_packet(data))
    conn.send(data)  # echo
    codop , valeur = process_packet(data)
    if (int(codop) == 2):
        data = valeur
    forward_voiture(data)

conn.close()
s.close()
    
    #le serveur se lance, il ecoute sur un port, il a une adresse ip
    #c'est lui qui crée le point d'accès
    #les telecommandes se connectent, leurs adresses ip sont pas importantes
    # les voitures se connectent, leurs adresses ips sont fixes selon les adresses mac
    #les telecommandes envoient la commande connect to car avec comme parametre
    
    #{'ip' : '192.168.1.101', 'port' : 8888 }
    