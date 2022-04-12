import threading

class Spy:
    def __init__(self, socket, network, name, key):
        self.name = name
        self.socket = socket
        self.network = network
        self.lastUpdate = ""
        self.key = key

    def main(self):
        while self.network.socketErrorDict[self.socket] == False:
            self.lastUpdate = self.network.recv(self.socket)

