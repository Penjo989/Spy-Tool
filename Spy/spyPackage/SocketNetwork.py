import socket
from spyPackage.Translator import *

class SocketNetwork:
    def __init__(self, translator, COM_PORT = 4096, connectionTimeout = 10, reportInterval = 0.2, buffer = 8):
        self.comIP = None
        self.COM_PORT = COM_PORT
        self.connectionTimeout = connectionTimeout
        self.reportInterval = reportInterval
        self.buffer = buffer
        self.connectionError = False
        self.spySocket = None
        self.lastMessageBuffer = ""
        self.translator = translator

    def setup(self):
        try:
            self.spySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as e:
            print(e)
            self.connectionError = True

    def send(self, data):
        try:
            #print(f"Sent {data}")
            self.spySocket.send(data.encode())
        except Exception as e:
            print(e)
            self.connectionError = True

    def recv(self):
        try:
            fullMsg = self.lastMessageBuffer
            while True:
                msg = self.spySocket.recv(self.buffer).decode()
                end = self.translator.END
                if end in fullMsg + msg:
                    fullMsg += msg[:msg.find(end) + len(end)]
                    self.lastMessageBuffer = msg[msg.find(end) + len(end):]
                    #print(f"Recv: {fullMsg}")
                    break

                elif len(msg) == 0:  #When the communicator disconnects spySocket.recv returns ""
                    self.connectionError = True
                    return
                fullMsg += msg
            return fullMsg
        except Exception as e:
            print(e)
            self.connectionError = True

    def connect(self, comIP):
        try:
            self.spySocket.settimeout(self.connectionTimeout)#set timeout
            self.spySocket.connect((comIP, self.COM_PORT))
            self.spySocket.setblocking(True)#disable timeout
            self.comIP = comIP
        except Exception as e:
            print(e)
            self.connectionError = True

    def disconnect(self):
        try:
            self.spySocket.close()
        except Exception as e:
            #print(e)
            pass

