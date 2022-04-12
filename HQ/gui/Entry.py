from gui.Box import *
from gui.EntryText import *

class Entry(Box):
    def __init__(self, relativePos, relativeSize, containerBox, id, surface, color = WHITE + LIGHT_BLUE):
        super().__init__(relativePos, relativeSize, containerBox, id, surface, color)
        self.MAX_TEXT_LENGTH = 15#MAX_TEXT_LENGTH
        self.text = EntryText([0, 0], [1, 1], self, id, surface, self.MAX_TEXT_LENGTH)

    def update(self, key):
        """
        updates the Text Object of the Entry
        :param key: given key
        """
        if key == "backspace":
            self.text.update(self.text.msg[:-1])
        elif len(self.text.msg) < self.MAX_TEXT_LENGTH:
            if key == "space":
                key = " "
            self.text.update(self.text.msg + key)

    def getText(self):
        return self.text.msg

    def draw(self):
        super().drawBox()
        self.text.draw()

