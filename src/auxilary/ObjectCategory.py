
from enum import IntEnum, auto


class ObjectCategory(IntEnum):
    PLAYER      = 0
    ENEMIES     = auto() # will fill automatically starting from 1, 2, 3, ...
    PROJECTILES = auto()
    STATIC      = auto()
    HUD         = auto()
    MISC        = auto()
