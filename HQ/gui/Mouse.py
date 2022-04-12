from gui.Pos import *

"""
Handles the mouse input
"""
class Mouse:
    def __init__(self):
        self.pos = Pos(0, 0)
        self.clicked = False
        self.clickUsed = False

    def update(self, cords):
        self.pos.setCords(cords)

    def mouseDown(self):
        self.clicked = True

    def mouseUp(self):
        self.clicked = False
        self.clickUsed = False