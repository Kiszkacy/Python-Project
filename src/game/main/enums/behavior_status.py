from enum import IntEnum, auto


class BehaviorStatus(IntEnum):
    IDLE = 0
    RUNNING = auto()
    INTERRUPTED = auto()
    NEXT_STATE = auto()
