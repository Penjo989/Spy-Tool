


class Communicator:
    def __init__(self, ip, COM_PORT = 4096):
        self.ip = ip
        self.port = COM_PORT
        self.randNum = None
        self.isAuthenticated = False
        self.key = None
        self.spies = []
        self.password = None