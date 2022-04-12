from spyPackage.Scanner import *
from spyPackage.SocketNetwork import *
from spyPackage.Mitm import *
from spyPackage.ArpSpoofer import *

class NetworkManager:
    def __init__(self, interface, spyIP, spyMac, subnet, translator):
        self.scanner = Scanner(subnet, interface, 10)
        self.socketNetwork = SocketNetwork(translator, reportInterval=0.2, connectionTimeout=5)
        self.mitm = Mitm(interface, spyIP)
        self.arpSpoofer = ArpSpoofer(spyMac, interface)
