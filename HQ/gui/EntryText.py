from gui.Text import *

class EntryText(Box):
    def __init__(self, relativePos, relativeSize, containerBox, id, surface, maxLength,  color = Color((0, 0, 0))):
        super().__init__(relativePos, relativeSize, containerBox, id, surface, color)
        self.maxLength = maxLength
        self.fontSize = self.getFontSize()
        self.font = pygame.font.SysFont(None, self.fontSize)
        self.update("")

    def getFontSize(self):
        size = 1
        msg = "m" * self.maxLength
        while True:
            self.font = pygame.font.SysFont(None, size + 1)
            msgSize = Size(self.font.size(msg)[0], self.font.size(msg)[1])
            if self.size <= msgSize:
                self.font = pygame.font.SysFont(None, size)
                return size
            size += 1
    def update(self, msg):
        self.msg = msg
        self.text = self.font.render(self.msg, True, self.color.rgb)

    def draw(self):
        self.surface.blit(self.text, self.pos.tuple())