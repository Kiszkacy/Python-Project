
from enum import IntEnum, auto


class ObjectCategory(IntEnum):
    PLAYER      = 0
    ENEMIES     = auto() # will fill automatically starting from 1, 2, 3, ...
    PROJECTILES = auto()
    STATIC      = auto()
    NEUTRAL     = auto()
    MISC        = auto()
    ITEMS       = auto()
    HUD         = auto()
