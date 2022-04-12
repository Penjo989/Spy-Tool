from gui.Box import *

class Text(Box):
    def __init__(self, relativePos, relativeSize, containerBox, id, surface, msg = "", color = Color((0, 0, 0))):
        super().__init__(relativePos, relativeSize, containerBox, id, surface, color)
        #pygame.font.init() important
        self.update(msg)

    def draw(self):
        self.surface.blit(self.text, self.pos.tuple())

    def update(self, msg):
        size = 1
        self.msg = msg
        while True:
            font = pygame.font.SysFont(None, size + 1)
            msgSize = Size(font.size(self.msg)[0], font.size(self.msg)[1])
            if self.size <= msgSize:
                font = pygame.font.SysFont(None, size)
                self.text = font.render(self.msg, True, self.color.rgb)
                return
            size += 1
