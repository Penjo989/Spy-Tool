from gui.Box import *

class PlainBox(Box):
    def __init__(self, relativePos, relativeSize, containerBox, id, surface, color = LIGHT_BLUE + WHITE + WHITE):
        self.relativePos = relativePos
        self.relativeSize = relativeSize
        super().__init__(relativePos, relativeSize, containerBox, id, surface, color)

    def resetContainerBox(self, containerBox):
        self.pos = containerBox.pos + containerBox.size.getPos(self.relativePos)
        self.size = containerBox.size.getSize(self.relativeSize)

    def drawOutLine(self, width = 2):
        color = BLACK + GRAY
        pygame.draw.rect(self.surface, color.rgb, (self.pos.x - width, self.pos.y - width,
                                                   self.size.width + 2 * width, self.size.height + 2 * width))