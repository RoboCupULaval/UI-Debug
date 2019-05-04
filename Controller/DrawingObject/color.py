from collections import namedtuple

ColorTuple = namedtuple('Color', 'red green blue')
class Color:
    RED = ColorTuple(red=255, green=0, blue=0)
    BLUE = ColorTuple(red=0, green=0, blue=255)
    SKY_BLUE = ColorTuple(red=100, green=150, blue=255)
    CYAN = ColorTuple(red=0, green=255, blue=255)
    YELLOW = ColorTuple(red=255, green=255, blue=0)
    CLEAR_YELLOW = ColorTuple(red=255, green=255, blue=100)
    BLACK = ColorTuple(red=0, green=0, blue=0)
    WHITE = ColorTuple(red=255, green=255, blue=255)
    DARK_GREEN_FIELD = ColorTuple(red=0, green=150, blue=0)
    GREEN_FIELD = ColorTuple(red=0, green=125, blue=0)
    CLEAR_ORANGE = ColorTuple(red=238, green=239, blue=168)
    ORANGE = ColorTuple(red=255, green=100, blue=0)
    DARK_ORANGE = ColorTuple(red=125, green=69, blue=25)