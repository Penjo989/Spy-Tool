from gui.Box import *
from gui.Text import *

class Button(Box):
    def __init__(self, relativePos, relativeSize, containerBox, id, surface, msg, color = BLUE + WHITE):
        super().__init__(relativePos, relativeSize, containerBox, id, surface, color)
        self.text = Text([0, 0], [1, 1], self, id, surface, msg)

    def draw(self):
        super().drawBox()
        self.text.draw()