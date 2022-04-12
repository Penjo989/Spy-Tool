from gui.Pos import *
from gui.PlainCell import *

class StationLink:
    def __init__(self, id, surface, color, plainCells):
        self.id = id
        self.surface = surface
        self.color = color
        self.plainCells = plainCells
        self.points = []
        self.isValid = None not in plainCells

    def __eq__(self, other):
        if type(other) == list:
            return other[0] in [self.plainCells[0].mainData, self.plainCells[1].mainData] \
                   and other[1] in [self.plainCells[0].mainData, self.plainCells[1].mainData]


    def updatePoints(self, points):
        self.points = points

    def draw(self):
        for i in range(len(self.points) - 1):
            pygame.draw.line(self.surface, self.color.rgb, self.points[i].tuple(), self.points[i + 1].tuple(), 3)
