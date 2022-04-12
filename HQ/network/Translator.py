import netStruct
from netStruct import Station


class Translator:
    def __init__(self):
        self.START = "STR"
        self.END = "END"
        self.RAW = "RAW"
        self.SECTION = "SCT"
        self.DIVIDER = "#"
        self.LINK = "~"
        self.SCAN = "SCN"
        self.SPOOFED = "SPF"
        self.MITM = "MTM"

        self.ADD_SPOOF = "ADDSPF"
        self.DELETE_SPOOF = "DELSPF"
        self.ADD_MITM = "ADDMTM"
        self.DELETE_MITM = "DELMTM"

        self.SPY = "SPY"
        self.HQ = "HQ"
        self.LOGGED_IN = "LOG"
        self.NOT_LOGGED_IN = "NOTLOG"

        self.CONNECTED_SPYS = "CONSPY"
        self.CON = "CON"
        self.REFRESH = "REF"

    def translateFrom(self, data):
        networkData, shellOutput = self.separate(data, self.RAW)

        scannedStations = []
        spoofs = []
        mitms = []

        networkData = networkData.split(self.SECTION)
        for data in networkData:
            splitedData = data.split(self.DIVIDER)
            if splitedData[0] == self.SCAN:
                for strStation in splitedData[1:]:
                    scannedStations.append(Station(strStation.split(self.LINK)[0], strStation.split(self.LINK)[1]))
            elif splitedData[0] == self.SPOOFED:
                for spoof in splitedData[1:]:
                    spoofs.append(spoof.split(self.LINK))
            elif splitedData[0] == self.MITM:
                for mitm in splitedData[1:]:
                    mitms.append(mitm.split(self.LINK))
        return scannedStations, spoofs, mitms, shellOutput
    def translateTo(self, scan, addSpoofs, delSpoofs, addMitm, delMitm, command):
        fullMsg = ""
        if scan:
            fullMsg += self.SCAN + self.SECTION
        fullMsg += self.ADD_SPOOF
        for spoof in addSpoofs:
            fullMsg += self.DIVIDER + spoof[0] + self.LINK + spoof[1]
        fullMsg += self.SECTION + self.DELETE_SPOOF
        for spoof in delSpoofs:
            fullMsg += self.DIVIDER + spoof[0] + self.LINK + spoof[1]
        fullMsg += self.SECTION + self.ADD_MITM
        for mitm in addMitm:
            fullMsg += self.DIVIDER + mitm[0] + self.LINK + mitm[1]
        fullMsg += self.SECTION + self.DELETE_MITM
        for mitm in delMitm:
            fullMsg += self.DIVIDER + mitm[0] + self.LINK + mitm[1]
        fullMsg += self.RAW + command
        return fullMsg
    def packData(self, data):
        return self.START + data + self.END

    def unpackData(self, data):
        return data[len(self.START):-len(self.END)]

    def makeAuthMessage(self, name):
        return self.HQ + self.DIVIDER + name

    def makeConMessage(self, spyName):
        return self.CON + self.DIVIDER + spyName

    def separate(self, string, subString):
        return string[:string.find(subString)], string[string.find(subString) + len(subString):]

