import time

from network.Translator import *
from network.Encrypter import *
from network.Communicator import *
from network.Spy import *
import threading
import socket

class Network:
    def __init__(self, connectionTimeout = 5, buffer = 8):
        self.translator = Translator()
        self.encrypter = Encrypter()
        self.spy = None
        self.communicator = None
        self.isConnecting = False
        self.isBusy = False
        self.isConnected = False
        self.hqName = None
        self.connectionTimeout = connectionTimeout
        self.buffer = buffer
        self.lastMessageBuffer = ""
        self.HQSocket = None
        self.isValid = self.setup()

    def setup(self):
        try:
            self.HQSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            return True
        except Exception as e:
            print(e)
            return False

    def restart(self):
        self.spy = None
        self.communicator = None
        try:
            self.HQSocket.shutdown(socket.SHUT_RDWR)
            self.HQSocket.close()
            self.isValid = self.setup()

        except Exception as e:
            print(e)

    def connect(self, ip, name):
        self.hqName = name
        self.communicator = Communicator(ip)
        connectThread = threading.Thread(target=self.connectionThread)
        connectThread.start()

    def connectionThread(self):
        self.isConnecting = True
        try:
            self.HQSocket.settimeout(self.connectionTimeout)  # set timeout
            self.HQSocket.connect((self.communicator.ip, self.communicator.port))
            self.HQSocket.setblocking(True)  # disable timeout
            self.isConnected = True
        except Exception as e:
            print(e)
        self.isConnecting = False

    def send(self, message, encrypt = True, pack=True):
        try:
            if encrypt:
                message = self.encrypter.encrypt(message)
            if pack:
                message = self.translator.packData(message)
            self.HQSocket.send(message.encode())
            #print(f"Sent: {message}")
        except Exception as e:
            print(e)
            self.isConnected = False

    def recv(self, decrypt = True, unPack = True):
        try:
            fullMsg = self.lastMessageBuffer
            while True:
                msg = self.HQSocket.recv(self.buffer).decode()
                if self.translator.END in fullMsg + msg:
                    fullMsg += msg[:msg.find(self.translator.END) + len(self.translator.END)]
                    self.lastMessageBuffer = msg[msg.find(self.translator.END) + len(self.translator.END):]
                    #print(f"Recv: {fullMsg}")
                    break
                elif len(msg) == 0:#wierd temporarty bug fix
                    self.isConnected = False
                    return ""
                fullMsg += msg
            if unPack:
                fullMsg = self.translator.unpackData(fullMsg)
            if decrypt:
                fullMsg = self.encrypter.decrypt(fullMsg)
            #print(f"Recv: {fullMsg}")
            return fullMsg
        except Exception as e:
            print(e)
            self.isConnected = False
            return ""

    def sendName(self):
        self.send(self.translator.makeAuthMessage(self.hqName), False)#send identity message

    def getRandNum(self):
        self.communicator.randNum = self.recv(False)  # get rand num

    def authenticate(self, password):
        self.isBusy = True
        self.communicator.key = self.encrypter.genKey(password, self.hqName)
        self.encrypter.setKey(self.communicator.key)
        self.send(self.communicator.randNum)#send encrypted randNUm
        result = self.recv(False)
        if self.isConnected == True and result == self.translator.LOGGED_IN:
            print("Logged In")
            self.communicator.password = password
            self.communicator.isAuthenticated = True
        self.isBusy = False

    def getSpies(self):
        while self.isConnected:
            msg = self.recv()
            if msg.split(self.translator.DIVIDER)[0] == self.translator.CONNECTED_SPYS:
                self.communicator.spies = msg.split(self.translator.DIVIDER)[1:]
                return

    def sendRefresh(self):
        self.send(self.translator.REFRESH)

    def connectToSpy(self, spyName):
        self.send(self.translator.makeConMessage(spyName))
        msg = self.recv()
        if msg == self.translator.LOGGED_IN:
            spyKey = self.encrypter.genKey(self.communicator.password, spyName)
            self.encrypter.setKey(spyKey)
            self.spy = Spy(spyName, spyKey)
            self.spy.connected = True
        else:
            self.communicator.spies = msg.split(self.translator.DIVIDER)[1:]

    def listenForUpdates(self):
        listenThread = threading.Thread(target=self.listenThread)
        listenThread.start()

    def listenThread(self):
        while self.isConnected and self.spy != None:
            try:
                msg = self.recv()
                if msg != self.translator.NOT_LOGGED_IN:
                    self.spy.lastUpdate = msg
                else:
                    self.spy = None
            except Exception as e:
                return

    def sendDisconnectMsg(self):
        self.send(self.translator.NOT_LOGGED_IN)
        self.encrypter.setKey(self.communicator.key)

    def sendCommand(self):
        scan, addSpoofs, delSpoofs, addMitm, delMitm, command = self.spy.getCommand()
        self.send(self.translator.translateTo(scan, addSpoofs, delSpoofs, addMitm, delMitm, command))
        self.spy.reset()

    def sendShellCommand(self, shellCommand):
        command = self.translator.translateTo(False, [], [], [], [], shellCommand)
        self.send(command)

    def disconnect(self):
        self.isConnected = False