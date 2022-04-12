
class StationLink:
    def __init__(self, sta1, sta2):
        self.sta1 = sta1
        self.sta2 = sta2

    def getMacs(self):
        return [self.sta1.staMac, self.sta2.staMac]
    def __eq__(self, other):
        return self.sta1 in [other.sta1, other.sta2] and self.sta2 in [other.sta1, other.sta2]

    def __str__(self):
        return f"{self.sta1.staIP}-{self.sta2.staIP}"

