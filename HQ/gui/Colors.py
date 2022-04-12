
class Color:
    def __init__(self, rgb):
        self.rgb = rgb

    def __add__(self, other):
        return Color(((self.rgb[0] + other.rgb[0]) / 2, (self.rgb[1] + other.rgb[1]) / 2,
                      (self.rgb[2] + other.rgb[2]) / 2))

    def __str__(self):
        return f"(R:{self.rgb[0]}, G:{self.rgb[1]}, B:{self.rgb[2]})"

WHITE = Color((255, 255, 255))
BLACK = Color((0, 0, 0))

RED = Color((255, 0, 0))
GREEN = Color((0, 255, 0))
BLUE = Color((0, 0, 255))

GRAY = BLACK + WHITE
LIGHT_GRAY = GRAY + WHITE
LIGHT_BLUE = Color((191, 221, 241))