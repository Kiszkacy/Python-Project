from __future__ import annotations
from abc import ABC, abstractmethod

# from src.game.main.interfaces.affectable import Affectable
from src.game.main.interfaces.processable import Processable
import src.game.main.interfaces.affectable as _ # NOTE: a wacky hack to avoid circular imports

class Effect(ABC, Processable):

    def __init__(self, target: _.Affectable) -> None:
        self.target: _.Affectable = target

    @abstractmethod
    def process(self, delta: float) -> None:
        pass

    @abstractmethod
    def activate(self) -> bool:
        pass

    @abstractmethod
    def deactivate(self) -> None:
        pass


if __name__ == '__main__':
    pass
