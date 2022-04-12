from gui.Box import *
from gui.Pos import *
from gui.Size import *
from gui.Text import *

class ListCell(Box):
    def __init__(self, containerBox, surface, mainData, sideData, color = GREEN + WHITE):
        super().__init__([0, 0], [0, 0], containerBox, "CELL", surface, color)
        self.mainData = mainData
        self.sideData = sideData
        self.mainText = Text([0, 0], [0.4, 0.7], self, "main", surface, self.mainData)
        self.sideText = Text([0.6, 0], [0.4, 0.7], self, "side", surface, self.sideData)

    def copyBox(self, box):
        self.size = box.size
        self.pos = box.pos
        self.mainText = Text([0, 0], [0.4, 0.7], self, "main", self.surface, self.mainData)
        self.sideText = Text([0.6, 0], [0.4, 0.7], self, "side", self.surface, self.sideData)

    def draw(self, selected = False, outLine = True):
        if outLine:
            self.drawOutLine()
        color = self.color
        if selected:
            color = color + BLACK
        pygame.draw.rect(self.surface, color.rgb, (self.pos.x, self.pos.y, self.size.width, self.size.height))
        self.mainText.draw()
        self.sideText.draw()

