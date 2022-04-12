from gui.Box import *
from gui.Pos import *
from gui.Size import *
from gui.Text import *

class PlainCell(Box):
    def __init__(self, containerBox, surface, mainData, color = BLUE + WHITE):
        super().__init__([0, 0], [0, 0], containerBox, "CELL", surface, color)
        self.mainData = mainData
        self.mainText = Text([0, 0], [0, 0], self, "main", surface, self.mainData)

    def copyBox(self, box):
        self.size = box.size
        self.pos = box.pos
        self.mainText = Text([0, 0], [1, 1], self, "main", self.surface, self.mainData)
        self.mainText.size = box.size
        self.mainText.pos = box.pos


    def draw(self, selected = False, outLine = True):
        if outLine:
            self.drawOutLine()
        color = self.color
        if selected:
            color = color + BLACK
        pygame.draw.rect(self.surface, color.rgb, (self.pos.x, self.pos.y, self.size.width, self.size.height))
        self.mainText.draw()

