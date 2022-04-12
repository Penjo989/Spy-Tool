from gui.Window import *
from gui.GraphicList import *
from gui.Timer import *

class SelectionWindow(Window):
    def __init__(self, surface, keyboard, mouse, network):
        super().__init__(surface, keyboard, mouse)
        self.network = network
        self.update = True
        self.connectTimer = Timer(1)
    def __call__(self):
        self.connectTimer.start()
        if self.update:
            self.updateSpies()
            self.update = False
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

            #print((self.network.spy != None and self.network.spy.connected), self.network.spy)
            if not self.network.isConnected or (self.network.spy != None and self.network.spy.connected):
                return

            boxUnderMouse = self.getBoxUnderMouse()
            self.handleBox(boxUnderMouse)

            self.draw()

    def handleClickedButton(self):
        if self.selectedBox.id == "list":
            self.selectedBox.handleClick(self.mouse.pos)
        elif self.connectTimer.isOver():
            if self.selectedBox.id == "disconnect":
                self.network.disconnect()
            elif self.selectedBox.id == "reload":
                self.network.sendRefresh()
                self.updateSpies()
            elif self.selectedBox.id == "control":
                if self.sections[1].selectedCell != None:
                    self.network.connectToSpy(self.sections[1].selectedCell.mainData)
    def setup(self):
        section1 = Section([0.01, 0.01], [0.35, 0.97], "sec1", self.surface, self.size)
        list = GraphicList([0.43, 0.1], [0.5, 0.8], "list", self.surface, self.size, 10)
        list.setCells(["1", "2", "3", "Spy", "assad", "asdsd", "asd"])

        headline = Text([0.1, 0.1], [0.8, 0.2], section1, "headline", self.surface, "Head-Quarters")
        chooseSpy = Text([0.1, 0.2], [0.45, 0.1], section1, "chooseSpy", self.surface, "Choose A Spy")

        disconnectButton = Button([0.65, 0.93], [0.3, 0.05], section1, "disconnect", self.surface, "Disconnect", RED)
        reloadButton = Button([0.05, 0.7], [0.5, 0.08], section1, "reload", self.surface, "Reload")
        controlButton = Button([0.05, 0.8], [0.5, 0.08], section1, "control", self.surface, "Control")

        section1.boxes = [headline, chooseSpy, disconnectButton, reloadButton, controlButton]
        self.sections.append(section1)
        self.sections.append(list)

    def updateSpies(self):
        self.network.getSpies()
        self.sections[1].setCells(self.network.communicator.spies)

