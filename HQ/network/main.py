from Network import *


def loop1():
    n = Network()
    if n.isValid:
        name = input("Enter name")
        while True:
            ip = input("Enter ip")
            n.connect(ip, name)
            while n.isConnecting:
                pass
            if n.isConnected:
                loop2(n)

def loop2(n):
    while n.isConnected:
        num = n.getRandNum()
        password = input("enter password")
        n.authenticate(password)
        if n.communicator.isAuthenticated:
            break
    if n.communicator.isAuthenticated:
        loop3(n)

def loop3(n):
    n.getSpies()
    while n.isConnected:
        ans = input("Enter spy name or type ret")
        if ans == "ret":
            n.sendRefresh()
            n.getSpies()
            print(n.communicator.spies)
        else:
            n.connectToSpy(ans)
            if n.spy != None and n.spy.connected:
                loop4(n)
def loop4(n):
    n.listenForUpdates()
    while n.isConnected and n.spy != None:
        ans = input("Enter Command or type dis")
        if ans == "dis":
            n.spy = None
        else:
            pass
    n.sendDisconnectMsg()
loop1()