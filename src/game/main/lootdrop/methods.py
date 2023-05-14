
from typing import Dict, Callable
from src.game.main.util.rand import randrange, one_in, permille_chance
from random import choices # NOTE: numpy is faster but requires floats

# pseudo-fake class-dict something
RollType: Dict[str, Callable] = {
    "ONE": lambda: 1,
    "CONSTANT": lambda amount: amount,
    "UNIFORM": lambda min_, max_: randrange(min_, max_),
    "ONE_IN": lambda amount: one_in(amount),
    "CHANCE": lambda amount: permille_chance(amount),
}

# pseudo-fake class-dict something
ChanceType: Dict[str, Callable] = {
    "ONE": lambda size: [randrange(0, size)],
    "ALL": lambda size: [i for i in range(size)],
    "ONE_IN": lambda size, chance: [i for i in range(size)] if one_in(chance) else [],
    "ONE_IN_EACH": lambda size, chance: [i for i in range(size) if one_in(chance)],
    "CHANCE": lambda size, chance: [i for i in range(size) if permille_chance(chance)],
    "CHANCE_EACH": lambda size, chance: [i for i in range(size) if permille_chance(chance)],
    "WEIGHTED": lambda size, weights: choices([i for i in range(size)], weights),
}


if __name__ == '__main__':
    pass
