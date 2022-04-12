from scapy.layers.dot11 import Dot11, Dot11EltRSN, RadioTap

from other.Timer import *
from scapy.all import *

class BssidFinder:
    def __init__(self, interface, ssid, sniffTimeOut = 10):
        self.ssid = ssid
        self.interface = interface
        self.sniffTimeOut = sniffTimeOut
        self.bssid = None
        self.apChannel = None
        self.isWPA2 = False
        self.MAX_CHANNEL = 11

    def run(self):
        try:
            channelThread = threading.Thread(target=self.switchChannels)
            channelThread.start()
            sniff(iface=self.interface, stop_filter=self.packetHandler, timeout=self.sniffTimeOut)
            if self.bssid != None and self.apChannel != None and self.isWPA2:
                return False
            return True
        except Exception as e:
            print(e)
            return True
    def switchChannels(self, interval = 1):
        channel = 1
        timer = Timer(self.sniffTimeOut)
        timer.start()
        while self.bssid == None and not timer.isOver():
            try:
                print(f"Changed to Channel{channel}")
                os.system(f"sudo iwconfig {self.interface} channel {channel}")
                time.sleep(interval)
                channel = channel + 1 if channel < self.MAX_CHANNEL else 1
            except Exception as e:
                print(e)

    def packetHandler(self, pkt):
        if pkt.haslayer(Dot11):  # refers to 802.11 protocol - wireless lan protocol
            if pkt.type == 0 and pkt.subtype == 8:  # if is a beacon type pkt
                # print(pkt.info.decode("utf-8") )
                if pkt.info.decode("utf-8") == self.ssid:  # pkt.info is the ssid from which the beacon was sent from
                    self.bssid = pkt.addr2
                    self.apChannel = self.freqToChannel(pkt[RadioTap].Channel)
                    self.isWPA2 = Dot11EltRSN in pkt
                    # pkt.show()
                    return True
        return False

    def freqToChannel(self, freq):
        return (freq - 2401) / 5