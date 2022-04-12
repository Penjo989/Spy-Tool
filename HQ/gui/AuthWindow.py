from gui.Window import *

class AuthWindow(Window):
    def __init__(self, surface, keyboard, mouse, network):
        super().__init__(surface, keyboard, mouse)
        self.network = network

    def __call__(self):
        self.network.sendName()
        self.network.getRandNum()
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

            if not self.network.isConnected or self.network.communicator.isAuthenticated:
                return
            self.updateStatus()


            boxUnderMouse = self.getBoxUnderMouse()
            self.handleBox(boxUnderMouse)

            self.draw()

    def handleClickedButton(self):
        if self.selectedBox.id == "disconnect":
            self.network.disconnect()
        elif self.selectedBox.id == "auth" and not self.network.isBusy:
            status = self.sections[0].getBoxByID("status")
            status.update("Authenticating...")
            status.color = BLUE
            password = self.sections[0].getBoxByID("passEntry").getText()
            self.network.authenticate(password)
            if not self.network.communicator.isAuthenticated:
                self.network.getRandNum()

    def setup(self):
        section1 = Section([0.03, 0.03], [0.94, 0.94], "sec1", self.surface, self.size)

        headline = Text([0.2, 0.1], [0.6, 0.2], section1, "headline", self.surface, "Head-Quarters")
        password = Text([0.2, 0.55], [0.2, 0.1], section1, "password", self.surface, "Password")
        author = Text([0.1, 0.9], [0.4, 0.05], section1, "author", self.surface, "Made By Eyal Angel")
        status = Text([0.6, 0.9], [0.4, 0.05], section1, "status", self.surface, color=BLUE)

        passwordEntry = Entry([0.45, 0.55], [0.3, 0.1], section1, "passEntry", self.surface)

        authButton = Button([0.8, 0.5], [0.15, 0.3], section1, "auth", self.surface, "Authenticate")
        disconnectButton = Button([0.8, 0.4], [0.15, 0.08], section1, "disconnect", self.surface, "Disconnect", RED + GRAY)

        section1.boxes = [headline,password,author, passwordEntry, authButton, disconnectButton, status]
        self.sections.append(section1)

    def updateStatus(self):
        if not self.network.isBusy:
            status = self.sections[0].getBoxByID("status")
            if status.msg != "":
                status.color = RED
                status.update("Failed To Authenticate.")