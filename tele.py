from struct import pack
from struct import unpack
from struct import calcsize as sizeof
import socket
import json
import threading
from tkinter import *

CONNECT_TO_CAR = 1
MOVE_CAR = 2
GET_MALUS = 3
SEND_MALUS = 4


# Cree un paquet avec le code adu type de message
def create_packet(op_code, data):
    return pack("!I{}s".format(len(data)), op_code, data.encode())
def process_packet(packet):
    try:
        code, bytes = unpack("!I{}s".format(len(packet)-sizeof("!I")), packet)
        return (code, bytes.decode("utf-8"))
    except:
        return (0, "")

TCP_IP, TCP_PORT, BUFFER_SIZE = '192.168.1.22', 1337, 1024
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(-1)
sock.connect((TCP_IP, TCP_PORT))
print(0)
sock.send(create_packet(CONNECT_TO_CAR, json.dumps({"ip": '192.168.1.101', "port": 8890})))
print(0.5)
data = sock.recv(BUFFER_SIZE)
print(0.8)
sock.send(create_packet(1000, "bla"))
data = sock.recv(BUFFER_SIZE)
print(1)
class MaluserThread(threading.Thread):
    def run(self):
        while True:
            data = sock.recv(BUFFER_SIZE)
            # if data != sock.send(create_packet(SEND_MALUS, ""))
            sock.send(create_packet(SEND_MALUS, ""))
class TeleKeyBoardCarController:
    RELEASED = 0
    PRESSED = 1
    KEYS_TO_ACTION = {'p': "forward", 'm': "backward", 'a':"left", 'z': "right"}
    def __init__(self, f, b, l, r, speed=0.3, m="s"):
        self.speed = speed
        self.m = m
        self.keys_status = {f: self.RELEASED, b: self.RELEASED, l: self.RELEASED, r: self.RELEASED}
        root = Tk()
        frame = Frame(root, width=100, height=100)
        frame.bind("<KeyPress>", self.keydown)
        frame.bind("<KeyRelease>", self.keyup)
        frame.pack()
        self.label_malused = Label(root, text="not malused")
        self.label_malused.pack()
        frame.focus_set()
        root.mainloop()
    def keydown(self, e):
        print("tele kd")
        print('up', e.char)
        if e.char in self.KEYS_TO_ACTION:
            self.keys_status[e.char] = self.PRESSED
            sock.send(create_packet(MOVE_CAR, e.char + ',' + str(self.speed) + ",press"))
            data = sock.recv(BUFFER_SIZE)
       
    def keyup(self, e):
        print("tele ku")
        print('down', e.char)
        if e.char in self.KEYS_TO_ACTION:
            self.keys_status[e.char] = self.RELEASED
            sock.send(create_packet(MOVE_CAR, e.char + ',' + str(self.speed) + ",release"))
            data = sock.recv(BUFFER_SIZE)
            # getattr(self, "stop_" + self.keys_to_action[e.char])()
            

MaluserThread().start()
print("Maluser thread started")

tele = TeleKeyBoardCarController("p", "m", "a", "z", 0.5)

del tele
