
"""
Handles the keyboard input

"""
class Keyboard:
    def __init__(self, keyInterval = 1):
        self.ENTRY_KEYS = "abcdefghijklmnopqrstuvwxyz0123456789."
        self.STATION_KEYS = ["right", "left", "up", "down"]
        self.pressedKey = ""
    def update(self, key):
        """
        updates the last pressed key
        :param key: last pressed key
        """
        if key in self.ENTRY_KEYS or key == "backspace" or key == "space" or key in self.STATION_KEYS:
            self.pressedKey = key
        else:
            self.pressedKey = ""
