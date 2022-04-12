from scapy.layers.l2 import ARP, Ether
from scapy.all import *
from other.Station import *
import threading
class Scanner:
    def __init__(self, subnet, interface, sniffTimeout = 10):
        self.subnet = subnet
        self.interface = interface
        self.sniffTimeout = sniffTimeout
        self.stations = []


        self.tempFunction()#shity temp function

    def scan(self):
        print("Scanning...")
        self.stations = []
        sniffThread = threading.Thread(target=self.sniffAnswers)
        sniffThread.start()
        self.sendArps()

    def sniffAnswers(self):
        sniff(prn=self.handlePacket, timeout=self.sniffTimeout, iface=self.interface)
        print(f"Scan Ended, Found {len(self.stations)} Stations.")

    def handlePacket(self, pkt):
        if ARP in pkt:
            if (pkt[ARP].op == 2):
                self.stations.append(Station(pkt[ARP].psrc, pkt[ARP].hwsrc))
    def sendArps(self):#Temporary
        for i in range(256):
            arppacket = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=(self.subnet + str(i)))
            sendp(arppacket, verbose=False, iface=self.interface)

    def getStationByIP(self, ip):
        for station in self.stations:
            if station.staIP == ip:
                return station
        return None


    def tempFunction(self):
        count = 0
        subnet = ""
        for char in self.subnet:
            if char == ".":
                count += 1
            subnet += char
            if count == 3:
                break
        self.subnet = subnet