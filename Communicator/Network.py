import socket
from Translator import *
from Encrypter import *


class Network:
    def __init__(self, ip, port, buffer = 8, timeout = 60):
        self.ip = ip
        self.port = port
        self.buffer = buffer
        self.comSocket = None
        self.timeout = timeout
        self.isValid = self.setup()
        self.socketErrorDict = {}
        self.lastMessageBuffer = ""

        self.encrypter = Encrypter()
        self.translator = Translator()

    def setup(self):
        try:
            self.comSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.comSocket.bind((self.ip, self.port))
            #self.comSocket.settimeout()#self.timeput
            self.comSocket.listen(1)

            return True
        except Exception as e:
            print(e)
            return False

    def accept(self):
        while True:
            try:
                clientSocket, address = self.comSocket.accept()
                print(f"{address} Is Trying To Connect.")
                self.socketErrorDict[clientSocket] = False
                return clientSocket
            except Exception as e:
            	print(e)
                

    def send(self, clientSocket, message, key = None, pack = True):
        try:
            #print(f"Sent: {message}")
            if key != None:
                message = self.encrypter.encrypt(message, key)
            if pack:
                message = self.translator.packData(message)
            clientSocket.send(message.encode())
        except Exception as e:
            print(e)
            self.socketErrorDict[clientSocket] = True

    def recv(self, clientSocket, key = None, unPack = True):
        try:
            fullMsg = self.lastMessageBuffer
            while True:
                msg = clientSocket.recv(self.buffer).decode()
                if "END" in fullMsg + msg:
                    fullMsg += msg[:msg.find("END") + 3]
                    self.lastMessageBuffer = msg[msg.find("END") + 3:]
            
                    break
                elif len(msg) == 0:#wierd temporarty bug fix
                    self.socketErrorDict[clientSocket] = True
                    return None
                fullMsg += msg
            if unPack:
                fullMsg = self.translator.unpackData(fullMsg)
            if key != None:
                fullMsg = self.encrypter.decrypt(fullMsg, key)
            #print(f"Recv: {fullMsg}")
            return fullMsg
        except Exception as e:
            print(e)
            self.socketErrorDict[clientSocket] = True
            return None


