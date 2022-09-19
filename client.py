import socket
import _pickle
from config import *


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (HOST, PORT)

    def connect(self, nick: str, color: str) -> int:
        self.client.connect(self.addr)
        new_string = nick+";"+color
        self.client.send(str.encode(new_string))
        # return id
        id = self.client.recv(8)
        return int(id.decode())

    def disconnect(self) -> None:
        self.client.close()

    def send(self, data: str) -> bytes:
        self.client.send(str.encode(data))
        reply = self.client.recv(2048 * 4)
        try:
            reply = _pickle.loads(reply)
        except Exception as e:str(e)
        return reply
