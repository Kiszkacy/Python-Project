
import random as r
import numpy as np
"""
NOTE: for future me
numpy generates random array faster than built-in methods
built-in method generate faster single digits
"""


def one_in(n: int) -> bool:
    return r.randint(1, n) == 1


def percentage_chance(chance: int) -> bool:
    return r.randint(1, 100) <= chance


def permille_chance(chance: int) -> bool:
    return r.randint(1, 1000) <= chance


def randrange(min_: int, max_: int) -> int:
    return r.randint(min_, max_)



if __name__ == '__main__':
    pass
