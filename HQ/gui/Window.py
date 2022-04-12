import pygame
import sys
from gui.Button import *
from gui.Entry import *
from gui.Section import *
from gui.GraphicList import *
import os

class Window:
    def __init__(self, surface, keyboard, mouse):
        self.surface = surface
        self.keyboard = keyboard
        self.mouse = mouse

        self.sections = []
        self.selectedBox = None
        self.size = Size(surface.get_width(), surface.get_height())
        self.setup()

    def __call__(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse.mouseUp()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse.mouseDown()
                if event.type == pygame.KEYDOWN:
                    self.keyboard.update(pygame.key.name(event.key))
                    self.handleSelectedBox()
            self.mouse.update(pygame.mouse.get_pos())

            boxUnderMouse = self.getBoxUnderMouse()
            self.handleBox(boxUnderMouse)

            self.draw()

    def getBoxUnderMouse(self):
        for section in self.sections:
            box = section.getBoxUnderMouse(self.mouse.pos)
            if box != None:
                return box
        return None

    def handleBox(self, box):
        if box == None:
            return
        box.mouseIsAbove = True
        if self.mouse.clicked and not self.mouse.clickUsed:
            self.selectedBox = box
            self.handleClickedButton()
            self.mouse.clickUsed = True

    def handleSelectedBox(self):
        if self.selectedBox == None:
            return
        if type(self.selectedBox) == Entry:
            self.selectedBox.update(self.keyboard.pressedKey)

    def draw(self):
        self.surface.fill(WHITE.rgb)
        for section in self.sections:
            section.draw()
        pygame.display.update()

    def handleClickedButton(self):
        pass

    def setup(self):
        section1 = Section([0, 0], [1, 1], "sec1", self.surface, self.size)
        self.sections.append(section1)

    def exit(self):
        os._exit(1)