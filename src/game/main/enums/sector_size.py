from enum import IntEnum, auto


class SectorSize(IntEnum):
    SMALL = 10  # size is expressed in chunks
    MEDIUM = 500
    BIG = 1000
    HUGE = 2000
    SUPER_HUGE = 10000
