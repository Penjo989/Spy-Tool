class Translator:
    def __init__(self):
        self.START = "STR"
        self.END = "END"

        self.DIVIDER = "#"

        self.SPY = "SPY"
        self.LOGGED_IN = "LOG"
        self.NOT_LOGGED_IN = "NOTLOG"

        self.CONNECTED_SPYS = "CONSPY"
        self.CON = "CON"
        self.REFRESH = "REF"

    def getIdentitiy(self, data):
        return data.split(self.DIVIDER)[1], data.split(self.DIVIDER)[0] == self.SPY

    def packData(self, data):
        return self.START + data + self.END

    def unpackData(self, data):
        return data[len(self.START):-len(self.END)]
