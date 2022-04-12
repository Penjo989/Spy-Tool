from gui.Section import *
from gui.Button import *
from gui.ListCell import *

class GraphicList(Section):
    def __init__(self, relativePos, relativeSize, id, surface, screenSize, boxNum, color = BLUE + GREEN):
        super().__init__(relativePos, relativeSize, id, surface, screenSize, color)
        self.boxNum = boxNum
        self.upButton = None
        self.downButton = None
        self.cells = []
        self.firstCellIndex = 0
        self.genBoxes()
        self.selectedCell = None

    def genBoxes(self):
        boxHeightRatio = 1 / (self.boxNum + 2)
        self.upButton = Button([0, 0], [1, boxHeightRatio], self, "up", self.surface, "up", LIGHT_BLUE)
        for i in range(1, self.boxNum + 1):
            self.boxes.append(Box([0, i * boxHeightRatio], [1, boxHeightRatio], self, str(i), self.surface, GREEN + BLUE))
        self.downButton = Button([0, 1 - boxHeightRatio], [1, boxHeightRatio], self, "down", self.surface, "down", LIGHT_BLUE)

    def getBoxUnderMouse(self, mousePos):
        if mousePos in self:
            for box in self.boxes + [self.upButton, self.downButton]:
                if mousePos in box:
                    box.mouseIsAbove = True
            return self

    def draw(self):
        super().draw()
        for cell in self.cells[self.firstCellIndex: self.firstCellIndex + self.boxNum]:
            if cell == self.selectedCell:
                cell.draw(True)
            else:
                cell.draw()
        self.upButton.draw()
        self.downButton.draw()

    def setCells(self, dataList):
        self.firstCellIndex = 0
        self.cells = []
        for data in dataList:
            self.cells.append(ListCell(self, self.surface, data, ""))

        if self.selectedCell not in self.cells:
            self.selectedCell = None
        self.asignBoxes()
    def asignBoxes(self):
        for i in range(len(self.boxes)):
            if i + self.firstCellIndex >= len(self.cells):
                return
            self.cells[i + self.firstCellIndex].copyBox(self.boxes[i])

    def handleClick(self, mousePos):
        if mousePos in self.upButton:
            if self.firstCellIndex > 0:
                self.firstCellIndex -= 1
                self.asignBoxes()
        elif mousePos in self.downButton:
            self.firstCellIndex += 1
            self.asignBoxes()
        for cell in self.cells[self.firstCellIndex: self.firstCellIndex + self.boxNum]:
            if mousePos in cell:
                self.selectedCell = cell
