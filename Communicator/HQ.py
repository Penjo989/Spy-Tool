import time
import threading
class HQ:
    def __init__(self, hqSocket, network, key, name, updateInterval = 0.2):
        self.hqSocket = hqSocket
        self.spy = None
        self.network = network
        self.key = key
        self.name = name
        self.updateInterval = updateInterval

    def main(self, spy):
        self.spy = spy
        authThread = threading.Thread(target=self.updateHQ)
        authThread.start()
        while not self.network.socketErrorDict[self.hqSocket]:
            msg = self.network.recv(self.hqSocket, self.spy.key)
            if self.network.socketErrorDict[self.hqSocket]:
                return
            if msg == self.network.translator.NOT_LOGGED_IN:
                self.spy = None
                break
            self.network.send(self.spy.socket, msg, self.spy.key)#tunnel msg to spy

    def updateHQ(self):
        while self.spy != None and not self.network.socketErrorDict[self.hqSocket] and not self.network.socketErrorDict[self.spy.socket]:
            self.network.send(self.hqSocket, self.spy.lastUpdate)#pack = False
            time.sleep(self.updateInterval)
        if self.spy != None and self.network.socketErrorDict[self.spy.socket]:
            self.network.send(self.hqSocket, self.network.translator.NOT_LOGGED_IN, self.spy.key)
