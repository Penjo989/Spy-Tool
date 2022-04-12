from gui.Pos import *

class Size:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def tuple(self):
        return (self.width, self.height)

    def getPos(self, relativePos):
        return Pos(self.width * relativePos[0], self.height * relativePos[1])

    def getSize(self, relativeSize):
        return Size(self.width * relativeSize[0], self.height * relativeSize[1])

    def __gt__(self, other):
        return self.width > other.width and self.height > other.height

    def __lt__(self, other):
        return self.width < other.width and self.height < other.height

    def __ge__(self, other):
        return self.width > other.width or self.height > other.height

    def __le__(self, other):
        return self.width < other.width or self.height < other.height

    def __str__(self):
        return f"(w: {self.width}, h: {self.height})"