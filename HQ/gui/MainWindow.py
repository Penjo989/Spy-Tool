from gui.Window import *
from gui.Plain import *
import os
import threading

class MainWindow(Window):
    def __init__(self, surface, keyboard, mouse, network):
        super().__init__(surface, keyboard, mouse)
        self.network = network
        self.clear = lambda: os.system('cls')

    def __call__(self):
        self.network.listenForUpdates()
        self.activateShell()
        self.sections[0].reset()
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

            if not self.network.isConnected:
                return

            boxUnderMouse = self.getBoxUnderMouse()
            self.handleBox(boxUnderMouse)

            if self.network.spy == None:
                self.network.sendDisconnectMsg()
                return


            self.updateWindow()
            self.draw()

    def handleClickedButton(self):
        status = self.sections[3].getBoxByID("status")
        if self.selectedBox.id == "plain":
            self.selectedBox.handleClick(self.mouse.pos)
        elif self.selectedBox.id == "reset":
            self.network.spy.reset()
            status.update("Command Reset")
        elif self.selectedBox.id == "exit":
            self.network.spy = None
        elif self.selectedBox.id == "addSpoof":
            target1 = self.sections[1].getBoxByID("spoof1").getText()
            target2 = self.sections[1].getBoxByID("spoof2").getText()
            self.network.spy.addSpoofs.append([target1, target2])
            status.update("Spoof Added")
        elif self.selectedBox.id == "delSpoof":
            target1 = self.sections[1].getBoxByID("spoof1").getText()
            target2 = self.sections[1].getBoxByID("spoof2").getText()
            self.network.spy.delSpoofs.append([target1, target2])
            status.update("Spoof Deleted")
        elif self.selectedBox.id == "addMitm":
            target1 = self.sections[2].getBoxByID("mitm1").getText()
            target2 = self.sections[2].getBoxByID("mitm2").getText()
            self.network.spy.addMitm.append([target1, target2])
            status.update("Mitm Added")
        elif self.selectedBox.id == "delMitm":
            target1 = self.sections[2].getBoxByID("mitm1").getText()
            target2 = self.sections[2].getBoxByID("mitm2").getText()
            self.network.spy.delMitm.append([target1, target2])
            status.update("Mitm Deleted")
        elif self.selectedBox.id == "scan":
            if self.selectedBox.color == RED:
                self.selectedBox.color = GREEN
                self.network.spy.scan = True
            else:
                self.selectedBox.color = RED
                self.network.spy.scan = False
        elif self.selectedBox.id == "sendCommand":
            self.network.sendCommand()
            status.update("Command Sent")
    def handleSelectedBox(self):
        if self.selectedBox == None:
            return
        if type(self.selectedBox) == Entry:
            self.selectedBox.update(self.keyboard.pressedKey)
        elif type(self.selectedBox) == Plain:
            self.selectedBox.handlePressedKey(self.keyboard.pressedKey)

    def updateWindow(self):
        try:
            self.sections[0].updateLinkPaths()
            scannedStations, spoofs, mitms, shellOutput = self.network.translator.translateFrom(self.network.spy.lastUpdate)
            strStations = []
            for sta in scannedStations:
                strStations.append(sta.staIP)
            self.sections[0].updateCells(strStations)
            if shellOutput != self.network.spy.lastShellOutput:
                self.clear()
                print(shellOutput)
                self.network.spy.lastShellOutput = shellOutput
            #print(f"Spoofs: {spoofs}\tMitm: {mitms}" )
            self.sections[0].updateLinks(spoofs, mitms)
        except Exception as e:
            #print(e)
            pass

    def activateShell(self):
        shellThread = threading.Thread(target=self.shellThread)
        shellThread.start()

    def shellThread(self):
        while self.network.spy != None and self.network.isConnected:
            command = input()
            if self.network.spy != None and self.network.isConnected:
                self.network.sendShellCommand(command)

    def setup(self):

        plain = Plain([0, 0], [1, 0.6], "plain", self.surface, self.size, 7, 10)
        plain.updateCells(["192.1213", "asdsd"])

        section1 = Section([0, 0.6], [0.25, 0.4], "sec1", self.surface, self.size)

        spoof1 = Entry([0.2, 0.3], [0.6, 0.1], section1, "spoof1", self.surface)
        spoof2 = Entry([0.2, 0.5], [0.6, 0.1], section1, "spoof2", self.surface)

        spoofTitle = Text([0.2, 0.08], [0.65, 0.2], section1, "spoofTitle", self.surface, "Spoof")

        addSpoof = Button([0.1, 0.8], [0.35, 0.13], section1, "addSpoof", self.surface, "add")
        delSpoof = Button([0.5, 0.8], [0.35, 0.13], section1, "delSpoof", self.surface, "delete")

        section1.boxes = [spoof1, spoof2, spoofTitle, addSpoof, delSpoof]
        section2 = Section([0.25, 0.6], [0.25, 0.4], "sec2", self.surface, self.size)

        mitm1 = Entry([0.2, 0.3], [0.6, 0.1], section2, "mitm1", self.surface)
        mitm2 = Entry([0.2, 0.5], [0.6, 0.1], section2, "mitm2", self.surface)

        mitmTitle = Text([0.2, 0.08], [0.65, 0.2], section2, "mitmTitle", self.surface, "Mitm")

        addMitm = Button([0.1, 0.8], [0.35, 0.13], section2, "addMitm", self.surface, "add")
        delMitm = Button([0.5, 0.8], [0.35, 0.13], section2, "delMitm", self.surface, "delete")

        section2.boxes = [mitm1, mitm2, mitmTitle, addMitm, delMitm]
        section3 = Section([0.5, 0.6], [0.5, 0.4], "sec3", self.surface, self.size)

        status = EntryText([0.05, 0.1], [0.55, 0.2], section3, "status", self.surface, 13, BLUE)

        scan = Button([0.8, 0.1], [0.15, 0.1], section3, "scan", self.surface, "scan", RED)
        exit = Button([0.8, 0.85], [0.15, 0.1], section3, "exit", self.surface, "exit")
        reset = Button([0.05, 0.85], [0.15, 0.1], section3, "reset", self.surface, "Reset")
        sendCommand = Button([0.3, 0.8], [0.35, 0.15], section3, "sendCommand", self.surface, "Send Command")

        section3.boxes = [scan, exit, sendCommand, reset, status]
        section1.shadow = False
        section2.shadow = False
        section3.shadow = False
        self.sections = [plain, section1, section2, section3]
