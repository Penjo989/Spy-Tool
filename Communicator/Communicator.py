import time
from Network import *
from Spy import *
from HQ import *
from Encrypter import *
from Translator import *

import random
import threading

class Communicator:
    def __init__(self, ip, port):
        self.password = None
        self.network = Network(ip, port)
        self.spies = []
        self.setup()

    def setup(self):
        print(self.getBanner())
        ans = input("Press Enter To Continue Or Type 'stop' To Exit The Communicator.\t")
        if ans != "stop":
            password = input("Please Enter Your Desired Password for The Communicator.\t")
            while password != "stop" and len(password) < 8:
                print("Your Password Must Be At Least 8 Digits/Characters Long.")
                password = input("Please Enter Password\t")
            if password != "stop":
                self.password = password
    def main(self):
        print(f"Communicator Up And Running With IP: {self.network.ip}")
        if self.network.isValid and self.password != None:
            print("Waiting For Spies/HQs.")
            while True:
                socket = self.network.accept()
                authThread = threading.Thread(target=self.authenticate, args = (socket,))
                authThread.start()

    def authenticate(self, socket):
        try:
            identity = self.network.recv(socket)#get name of connecting client
            if self.network.socketErrorDict[socket]:
                return

            name, isSpy = self.network.translator.getIdentitiy(identity)
            if self.getSpyByName(name) != None:#name already exists
                socket.close()
                return
            key = self.network.encrypter.genKey(self.password, name)#generate key
            while True:
                randNumber = str(random.randint(0, 429497295))#generate 32bit number
                self.network.send(socket, randNumber)#sendnumber
                if self.network.socketErrorDict[socket]:
                    return
                ans = self.network.recv(socket)#get answer
                if not self.network.socketErrorDict[socket]:
                    decryptedNumber = self.network.encrypter.decrypt(ans, key)#decrypt answer
                    if decryptedNumber == randNumber:#check if answer correct
                        self.network.send(socket, self.network.translator.LOGGED_IN)
                        if self.network.socketErrorDict[socket]:
                            return
                        break
                    else:
                        self.network.send(socket, self.network.translator.NOT_LOGGED_IN)
                        if self.network.socketErrorDict[socket]:
                            return
            if isSpy == True:
                print(f"A Spy Named {name} Has Connected!")
                newSpy = Spy(socket, self.network, name, key)
                self.spies.append(newSpy)
                newSpy.main()
                self.spies.remove(newSpy)
                print(f"A Spy Named {name} Has Disconnected.")
            else:
                print(f"An HQ Named {name} Has Connected!")
                newHQ = HQ(socket, self.network, key, name)
                self.hqThread(newHQ)
                print(f"An HQ Named {name} Has Disconnected.")
        except Exception as e:
            print(e)

    def hqThread(self, hq):
        try:
            while self.network.socketErrorDict[hq.hqSocket] == False:
                spyListMsg = self.network.translator.CONNECTED_SPYS
                for spy in self.spies:
                    spyListMsg += self.network.translator.DIVIDER + spy.name
                self.network.send(hq.hqSocket, spyListMsg, hq.key)#send list of online spys like this STRCONSPY#SPY1#SPY2END
                if self.network.socketErrorDict[hq.hqSocket]:
                    return
                ans = self.network.recv(hq.hqSocket, hq.key)
                if self.network.socketErrorDict[hq.hqSocket]:
                    return
                ans = ans.split(self.network.translator.DIVIDER)
                if ans[0] == self.network.translator.CON:
                    spy = self.getSpyByName(ans[1])
                    if spy != None:
                        print(f"An HQ Named {hq.name} Has Connected To A Spy Named {spy.name}.")
                        self.network.send(hq.hqSocket, self.network.translator.LOGGED_IN, hq.key)
                        hq.main(spy)
                        print(f"An HQ Named {hq.name} Has Disonnected From A Spy Named {spy.name}.")
                        time.sleep(hq.updateInterval)#wait for thread to end
        except Exception as e:
            print(e)

    def getSpyByName(self, spyName):
        for spy in self.spies:
            if spy.name == spyName:
                return spy
        return None

    def getBanner(self):
        try:
            f = open("CommunicatorBanner", "r")
            banner = f.read()
            f.close()
            return banner
        except:
            return "Hello"
