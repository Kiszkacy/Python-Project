from __future__ import annotations

from typing import List, Type

import src.game.main.effects.effect as _ # NOTE: a wacky hack to avoid circular imports


class Affectable:

    def __init__(self) -> None:
        self.effects: List[_.Effect] = []

    def add_effect(self, effect: _.Effect) -> bool:
        self.effects.append(effect)
        # TODO add behavior

    def remove_effect(self, effect: Type[_.Effect]) -> bool:
        self.effects = [e for e in self.effects if type(e) != effect] # TODO this is very bad redo in the future

    def has_effect(self, effect: Type[_.Effect]) -> bool:
        return any(isinstance(e, type(effect)) for e in self.effects)


if __name__ == '__main__':
    pass
