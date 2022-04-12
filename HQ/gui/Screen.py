from gui.Size import *
from gui.Keyboard import *
from gui.Mouse import *
from gui.LoginWindow import *
from gui.AuthWindow import *
from gui.SelectionWindow import *
from gui.MainWindow import *
import pygame

class Screen:
    def __init__(self, width, height, caption, network):
        self.screenSize = Size(width, height)
        self.caption = caption
        self.network = network
        self.surface = None
        self.keyboard = Keyboard()
        self.mouse = Mouse()
        self.loginWindow = None
        self.authWindow = None
        self.selectionWindow = None
        self.mainWindow = None

        self.setup()

    def setup(self):
        pygame.init()
        self.surface = pygame.display.set_mode(self.screenSize.tuple())
        pygame.display.set_caption(self.caption)

        programIcon = pygame.image.load('src\icon.png')
        pygame.display.set_icon(programIcon)

        self.loginWindow = LoginWindow(self.surface, self.keyboard, self.mouse, self.network)
        self.authWindow = AuthWindow(self.surface, self.keyboard, self.mouse, self.network)
        self.selectionWindow = SelectionWindow(self.surface, self.keyboard, self.mouse, self.network)
        self.mainWindow = MainWindow(self.surface, self.keyboard, self.mouse, self.network)

    def display(self):
        while self.network.isValid:
            self.loginWindow()
            self.authWindow()
            while self.network.isConnected:
                self.selectionWindow()
                if self.network.spy != None and self.network.spy.connected:
                    self.mainWindow()
            self.network.restart()
