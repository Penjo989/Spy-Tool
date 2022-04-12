from netStruct.StationLink import *

class Station:
    def __init__(self, staIP, staMac):
        self.staIP = staIP
        self.staMac = staMac

    def __str__(self):
        return f"staIP: {self.staIP}\tstaMac: {self.staMac}"

    def __add__(self, other):
        return StationLink(self, other)

    def __eq__(self, other):
        if other == None:
            return False
        return other.staIP == self.staIP and other.staMac == self.staMac