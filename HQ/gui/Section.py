from gui.Box import *

class Section(Box):
    def __init__(self, relativePos, relativeSize, id, surface, screenSize, color = LIGHT_BLUE):
        self.size = screenSize.getSize(relativeSize)
        self.pos = screenSize.getPos(relativePos)
        self.color = color

        self.mouseIsAbove = False
        self.id = id
        self.surface = surface
        self.boxes = []
        self.shadow = True

    def draw(self):
        super().drawBox()
        for box in self.boxes:
            if type(box) == Box:
                box.drawBox()
            else:
                box.draw()

    def getBoxByID(self, id):
        for box in self.boxes:
            if box.id == id:
                return box

    def getBoxUnderMouse(self, mousePos):
        if mousePos in self:
           for box in self.boxes:
               if mousePos in box:
                   return box
        return None

    def drawOutLine(self, width = 5):
        if self.shadow:
            color = self.color + BLACK
            pygame.draw.rect(self.surface, color.rgb, (self.pos.x + width, self.pos.y + width,
                                                       self.size.width + width, self.size.height + width))
        else:
            super().drawOutLine()