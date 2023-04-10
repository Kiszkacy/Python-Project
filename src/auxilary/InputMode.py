
from enum import IntEnum, auto


class InputMode(IntEnum):
    INGAME      = 0
    MENU        = auto() # will fill automatically starting from 1, 2, 3, ...
    CONSOLE     = auto()
