import random

from gui.PlainCell import *
from gui.Section import *
from gui.PlainBox import *
from gui.Button import *
from gui.StationLink import *

class Plain(Section):
    def __init__(self, relativePos, relativeSize, id, surface, screenSize, cellRows, cellColumns):
        super().__init__(relativePos, relativeSize, id, surface, screenSize)
        self.plainBoxes = []
        self.cells = []

        self.spoofLinks = []
        self.mitmLinks = []

        self.cellRows = cellRows
        self.cellColumns = cellColumns
        self.selectedCell = None
        self.genBoxes()

    def genBoxes(self):
        boxHeightRatio = 1 / self.cellRows
        boxWidthRatio = 1 / self.cellColumns

        for i in range(self.cellRows):
            row = []
            for j in range(self.cellColumns):
                row.append(PlainBox([j * boxWidthRatio, i * boxHeightRatio], [boxWidthRatio, boxHeightRatio],
                                    self, f"{j},{i}", self.surface))
            self.plainBoxes.append(row)

    def updateCells(self, strCells):
        newCells = []
        oldStrCells = []
        for cell in self.cells:
            if cell.mainData in strCells:
                newCells.append(cell)
            oldStrCells.append(cell.mainData)
        for strCell in strCells:
            if strCell not in oldStrCells:
                cell = PlainCell(self, self.surface, strCell)
                cell.copyBox(self.getRandPlainBox())
                newCells.append(cell)
        self.cells = newCells


    def getRandPlainBox(self):
        return self.plainBoxes[random.randint(0, self.cellRows - 1)][random.randint(0, self.cellColumns - 1)]


    def draw(self):
        super().draw()
        for row in self.plainBoxes:
            for box in row:
                box.drawBox()
        for cell in self.cells:
            cell.draw(outLine = False)
        for link in self.spoofLinks + self.mitmLinks:
            link.draw()

    def getBoxUnderMouse(self, mousePos):
        if mousePos in self:
           for row in self.plainBoxes:
               for box in row:
                   if mousePos in box:
                       box.mouseIsAbove = True
           return self

    def handleClick(self, mousePos):
        self.selectedCell = None

        for cell in self.cells:
            if mousePos in cell:
                self.selectedCell = cell

    def handlePressedKey(self, key):
        if self.selectedCell == None:
            return
        row, column = self.getPosIndexes(self.selectedCell.pos)
        if key == "w" and row > 0:
            self.selectedCell.copyBox(self.plainBoxes[row - 1][column])
        elif key == "s" and row < self.cellRows - 1:
            self.selectedCell.copyBox(self.plainBoxes[row + 1][column])
        elif key == "a" and column > 0:
            self.selectedCell.copyBox(self.plainBoxes[row][column - 1])
        elif key == "d" and column < self.cellColumns - 1:
            self.selectedCell.copyBox(self.plainBoxes[row][column + 1])

    def getPosIndexes(self, pos):
        for row in range(self.cellRows):
            for column in range(self.cellColumns):
                if pos == self.plainBoxes[row][column].pos:
                    return row, column

    def updateLinks(self, spoofs, mitms):
        newSpoofLinks = []
        for spoof in self.spoofLinks:
            for spoofList in spoofs:
                if spoof == spoofList:
                    newSpoofLinks.append(spoof)
                    break
        for spoofList in spoofs:
            equals = False
            for spoof in newSpoofLinks:
                if spoof == spoofList:
                    equals = True
                    break
            if not equals:
                newLink = StationLink("staLink", self.surface, GREEN,
                                                 [self.getCellByStr(spoofList[0]), self.getCellByStr(spoofList[1])])
                if newLink.isValid:
                    newSpoofLinks.append(newLink)
        self.spoofLinks = newSpoofLinks

        newMitmLinks = []
        for mitm in self.mitmLinks:
            for mitmList in mitms:
                if mitm == mitmList:
                    newMitmLinks.append(mitm)
                    break
        for mitmList in mitms:
            equals = False
            for mitm in newMitmLinks:
                if mitm == mitmList:
                    equals = True
                    break
            if not equals:
                newLink = StationLink("staLink", self.surface, RED,
                                                 [self.getCellByStr(mitmList[0]), self.getCellByStr(mitmList[1])])
                if newLink.isValid:
                    newMitmLinks.append(newLink)
        self.mitmLinks = newMitmLinks

    def calcLinkPath(self, link):
        points = [link.plainCells[0].pos]
        startY, startX = self.getPosIndexes(link.plainCells[0].pos)
        endY, endX = self.getPosIndexes(link.plainCells[1].pos)
        #print(f"Start: {self.getPosIndexes(link.plainCells[0].pos)}, \t\tEND: {self.getPosIndexes(link.plainCells[1].pos)}")

        while startX != endX:
            if startX > endX:
                startX -= 1
            else:
                startX += 1
            points.append(self.plainBoxes[startY][startX].pos)


        while startY != endY:
            if startY > endY:
                startY -= 1
            elif startY < endY:
                startY += 1
            points.append(self.plainBoxes[startY][startX].pos)

        link.updatePoints(points)

    def updateLinkPaths(self):
        for link in self.mitmLinks + self.spoofLinks:
            self.calcLinkPath(link)

    def getCellByStr(self, string):
        for cell in self.cells:
            if cell.mainData == string:
                return cell


    def reset(self):
        self.cells = []
        self.spoofLinks = []
        self.mitmLinks = []