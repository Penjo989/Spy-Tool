from scapy.all import *
import subprocess, os, time, binascii



class Handshake:
    def __init__(self, PKT1, PKT2):
        self.PKT1 = PKT1
        self.PKT2 = PKT2
        self.apMac = ""
        self.staMac = ""
        self.aNonce = None
        self.sNonce = None
        self.mic = None
        self.isValid= self.extractValues()

    def extractValues(self):
        try:
            self.apMac = self.PKT1.addr2#src mac
            self.staMac = self.PKT2.addr2#src mac
            self.aNonce = self.getNonce(self.PKT1)
            self.sNonce = self.getNonce(self.PKT2)
            self.mic = self.getMic(self.PKT2)
            return True
        except:
            return False

    def getNonce(self, pkt):
        return pkt[Raw].load[13:45]

    def getMic(self, pkt):
        return binascii.hexlify(pkt[Raw].load)[154:186]#.decode("utf-8")

    def __str__(self):
        return f"apMac:\t{self.apMac}\nstaMac:\t{self.staMac}\naNonce:\t{self.aNonce}\nsNonce:\t{self.sNonce}\nmic:\t{self.mic}\n"