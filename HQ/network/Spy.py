

class Spy:
    def __init__(self, name, key):
        self.name = name
        self.key = key
        self.connected = True
        self.lastUpdate = ""
        self.lastShellOutput = ""
        self.scan = False
        self.addSpoofs = []
        self.delSpoofs =[]
        self.addMitm = []
        self.delMitm = []

    def getCommand(self):
        return self.scan, self.addSpoofs, self.delSpoofs, self.addMitm, self.delMitm, ""

    def reset(self):
        self.addSpoofs = []
        self.delSpoofs = []
        self.addMitm = []
        self.delMitm = []

