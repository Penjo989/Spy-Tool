import pygame
from gui.Colors import *
from gui.Size import *

class Box:
    def __init__(self, relativePos, relativeSize, containerBox, id, surface, color):
        self.color = color
        self.pos = containerBox.pos + containerBox.size.getPos(relativePos)
        self.size = containerBox.size.getSize(relativeSize)
        self.id = id
        self.surface = surface
        self.mouseIsAbove = False

    def __contains__(self, pos):
        if pos.x >= self.pos.x and pos.x <= self.pos.x + self.size.width:
            if pos.y >= self.pos.y and pos.y <= self.pos.y + self.size.height:
                return True
        return False

    def __str__(self):
        return f"ID: {self.id}\tPOS: {self.pos}\tSIZE: {self.size}\tCOLOR: {self.color}"

    def drawBox(self):
        self.drawOutLine()
        color = self.color
        if self.mouseIsAbove:
            color = color + BLACK
            self.mouseIsAbove = False
        pygame.draw.rect(self.surface, color.rgb, (self.pos.x, self.pos.y, self.size.width, self.size.height))

    def drawOutLine(self, width = 3):
        color = self.color + BLACK
        pygame.draw.rect(self.surface, color.rgb, (self.pos.x - width, self.pos.y - width,
                                                   self.size.width + 2 * width, self.size.height + 2 * width))