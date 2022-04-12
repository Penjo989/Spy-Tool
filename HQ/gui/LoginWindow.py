from gui.Window import *

class LoginWindow(Window):
    def __init__(self, surface, keyboard, mouse, network):
        super().__init__(surface, keyboard, mouse)
        self.network = network

    def __call__(self):
        self.sections[0].getBoxByID("status").update("")
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

            if self.network.isConnected:
                return
            self.updateStatus()

            boxUnderMouse = self.getBoxUnderMouse()
            self.handleBox(boxUnderMouse)

            self.draw()

    def handleClickedButton(self):
        if self.selectedBox.id == "connect" and not self.network.isConnecting:
            ip = self.sections[0].getBoxByID("ipEntry").getText()
            name = self.sections[0].getBoxByID("nameEntry").getText()
            self.network.connect(ip, name)
            status = self.sections[0].getBoxByID("status")
            status.color = BLUE
            status.update("Connecting...")

    def setup(self):
        section1 = Section([0.03, 0.03], [0.94, 0.94], "sec1", self.surface, self.size)

        headline = Text([0.2, 0.1], [0.6, 0.2], section1, "headline", self.surface, "Head-Quarters")
        ip = Text([0.2, 0.5], [0.1, 0.1], section1, "ip", self.surface, "IP")
        name = Text([0.2, 0.7], [0.2, 0.1], section1, "name", self.surface, "Name")
        author = Text([0.1, 0.9], [0.4, 0.05], section1, "author", self.surface, "Made By Eyal Angel")
        status = Text([0.6, 0.9], [0.4, 0.05], section1, "status", self.surface, color = BLUE)

        ipEntry = Entry([0.45, 0.5], [0.3, 0.1], section1, "ipEntry", self.surface)
        nameEntry = Entry([0.45, 0.7], [0.3, 0.1], section1, "nameEntry", self.surface)

        connectButton = Button([0.8, 0.5], [0.15, 0.3], section1, "connect", self.surface, "Connect")

        section1.boxes = [headline, ip, name, author, ipEntry, nameEntry, connectButton, status]
        self.sections.append(section1)

    def updateStatus(self):
        if not self.network.isConnecting:
            status = self.sections[0].getBoxByID("status")
            if status.msg != "":
                status.color = RED
                status.update("Failed To Connect.")