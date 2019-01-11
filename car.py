import socket
from struct import pack
from struct import unpack
from struct import calcsize as sizeof
from carcontroller import CarController
import RPi.GPIO as GPIO 

try:

    print(1)
    TCP_IP, TCP_PORT, BUFFER_SIZE = '192.168.1.101', 8891, 1024
    print(2)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(3)
    sock.bind((TCP_IP, TCP_PORT))
    print(4)
    sock.listen(10)
    print(5)
    conn, addr = sock.accept()
    print(6)

    CONNECT_TO_CAR = 1
    MOVE_CAR = 2
    GET_MALUS = 3
    SEND_MALUS = 4


    # Extrait le code du type de message ainsi que les donnees du paquet
    def process_packet(packet):
        try:
            code, bytes = unpack("!I{}s".format(len(packet)-sizeof("!I")), packet)
            return (code, bytes.decode("utf-8"))
        except:
            return (0, "")


    class ListeningCarController(CarController):
        def listen(self):
            while True:
                print(100)
                packet = conn.recv(1024)
                conn.send(packet)
                print(101)
                print("car received", packet)
                #code, content = process_packet(packet)
                try:
                    code, content = MOVE_CAR, packet.decode("utf-8")
                    print("car received", code, content)
                    if code == MOVE_CAR:
                        key, speed, press_or_release = content.split(",")
                        if press_or_release == "press":
                            getattr(self, self.KEYS_TO_ACTION[key])(1)
                        if press_or_release == "release":
                            getattr(self, "stop_" + self.KEYS_TO_ACTION[key])()
                except:
                    code, content = process_packet(packet)
                    if code == SEND_MALUS:
                        self.malus(1)
    print(7)
    car = ListeningCarController()
    print(8)
    car.stop()
    car.listen()
    print(9)
    
except Exception as e:
    print(10)
    print(e)
    try:
        conn.close()
    except:
        pass
    raise
finally:
    try:
        del car
    except:
        pass