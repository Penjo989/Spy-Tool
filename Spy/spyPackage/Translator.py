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
        self.LOGGED_IN = "LOG"
        self.NOT_LOGGED_IN = "NOTLOG"
    def translateTo(self, scannedStations, spoofLinks, mitmLinks, shellOutput):
        finalMsg = ""
        if scannedStations != None:
            msg = ""
            for sta in scannedStations:
                msg += self.DIVIDER + sta.staIP + self.LINK + sta.staMac
            finalMsg += self.SCAN + msg + self.SECTION

        msg = ""
        for link in spoofLinks:
            msg += self.DIVIDER + link.sta1.staIP + self.LINK + link.sta2.staIP
        finalMsg += self.SPOOFED + msg + self.SECTION

        msg = ""
        for link in mitmLinks:
            msg += self.DIVIDER + link.sta1.staIP + self.LINK + link.sta2.staIP
        finalMsg += self.MITM + msg

        finalMsg += self.RAW + shellOutput

        return finalMsg

    def translateFrom(self, data):
        networkData, command = self.separate(data, self.RAW)

        scan = False
        addSpoofs = []
        delSpoofs = []
        addMitm = []
        delMitm = []


        networkSections = networkData.split(self.SECTION)

        for section in networkSections:
            sectionData = section.split(self.DIVIDER)
            if sectionData[0] == self.SCAN:
                scan = True
            elif sectionData[0] == self.ADD_SPOOF:
                for spoof in sectionData[1:]:
                    addSpoofs.append(spoof.split(self.LINK))
            elif sectionData[0] == self.DELETE_SPOOF:
                for spoof in sectionData[1:]:
                    delSpoofs.append(spoof.split(self.LINK))
            elif sectionData[0] == self.ADD_MITM:
                for mitm in sectionData[1:]:
                    addMitm.append(mitm.split(self.LINK))
            elif sectionData[0] == self.DELETE_MITM:
                for mitm in sectionData[1:]:
                    delMitm.append(mitm.split(self.LINK))
        return scan, addSpoofs, delSpoofs, addMitm, delMitm, command

    def showIdentity(self, name):
        return self.SPY + self. DIVIDER + name



    def packData(self, data):
        return self.START + data + self.END

    def unpackData(self, data):
        return data[len(self.START):-len(self.END)]

    def separate(self, string, subString):
        return string[:string.find(subString)], string[string.find(subString) + len(subString):]

