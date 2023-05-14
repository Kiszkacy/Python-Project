
from typing import Dict, Callable
from src.game.main.util.rand import randrange, one_in, permille_chance
from random import choices # NOTE: numpy is faster but requires floats

# pseudo-fake class-dict something
RollType: Dict[str, Callable] = {
    "ONE": lambda: 1,
    "CONSTANT": lambda amount: amount,
    "UNIFORM": lambda min_, max_: randrange(min_, max_),
    "ONE_IN": lambda chance: 1 if one_in(chance) else 0,
    "CHANCE": lambda chance: 1 if permille_chance(chance) else 0,
}

# pseudo-fake class-dict something
ChanceType: Dict[str, Callable] = {
    "ONE": lambda size: [randrange(0, size-1)],
    "ALL": lambda size: [i for i in range(size)],
    "ONE_IN": lambda size, chance: [i for i in range(size)] if one_in(chance) else [],
    "ONE_IN_EACH": lambda size, chance: [i for i in range(size) if one_in(chance)],
    "CHANCE": lambda size, chance: [i for i in range(size)] if permille_chance(chance) else [],
    "CHANCE_EACH": lambda size, chance: [i for i in range(size) if permille_chance(chance)],
    "WEIGHTED": lambda size, weights: choices([i for i in range(size)], weights), # TODO i dont know if this works tbh
}


if __name__ == '__main__':
    pass
