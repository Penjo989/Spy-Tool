from preSpy.SetupManager import *
from spyPackage.Spy import *

class ProgramManager:
    def __init__(self, bannerDir):
        self.setupManager = SetupManager()
        self.bannerDir = bannerDir
        self.requirements = "In Order To Run The Spy Properly You Need To Run It On A Kali Linux Machine.\n" \
                            "Note: If You Want To Perform A Brute-Force Attack On A WPA2-PSK Access-Point\n" \
                            "You Must Choose A Wireless Interface That Supports Monitor Mode.\n" \
                            "Your Interface Doesn't Have To Support Packet Injecting But Without Packet Injecting\n" \
                            "Capturing The Four Way Handshake Might Take A While."

    def main(self):
        if self.setupManager.connected:
            spy = Spy(self.setupManager.interface, self.setupManager.interfaceIP, self.setupManager.interfaceMac)
            spy.main()


    def setup(self):
        print(self.getBanner())
        ans = input("Press ENTER To Continue Or Type 'info' For Information Regarding Running The Spy.\n"
                    "You Can Exit The Program By Typing 'stop'.\t")
        if ans == "info":
            print(self.requirements)
            ans = input("Press Enter To Continue.\t")
        while ans != "stop":
            self.setupManager.nextInterface()
            if self.setupManager.stop:
                print("Closing Program.\t")
                break
            if self.setupManager.isConnected(self.setupManager.interface):
                self.setupManager.connected = True
                print(f"The Interface {self.setupManager.interface} Is Connected To The Internet, Setup Successful.\t")
                break
            print(f"The Interface {self.setupManager.interface} Is Not Connected To The Internet.\t")
            self.setupManager.wpaAttack()
            if self.setupManager.stop:
                print("Closing Program.\t")
                break
            loop = input("Would You Want To Try A Different Interface?[Y][N]\t")
            while loop not in ["y", "n", "Y", "N"]:
                loop = input("Invalid Answer, Try Again.\t")
            if loop in ["n", "N"]:
                print("Closing Program.\t")
                break

    def getBanner(self):
        try:
            f = open(self.bannerDir, "r")
            banner = f.read()
            f.close()
            return banner
        except Exception as e:
            print(e)
            return "Welcome"

