
class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def tuple(self):
        return (self.x, self.y)

    def setCords(self, cords):
        self.x = cords[0]
        self.y = cords[1]

    def __add__(self, other):
        return Pos(other.x + self.x, other.y + self.y)

    def __str__(self):
        return f"({self.x}, {self.y})"
