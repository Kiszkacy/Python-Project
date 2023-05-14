from abc import abstractmethod

from src.game.main.effects.effect import Effect
from src.game.main.interfaces.affectable import Affectable


class ActiveEffect(Effect):

    def __init__(self, target: Affectable, lifetime: float, ticks_per_sec: int) -> None:
        super(ActiveEffect, self).__init__(target)
        self.ticks_per_sec: int = ticks_per_sec
        self.tick_delay: float = 1.0 / self.ticks_per_sec
        self.lifetime: float = lifetime
        # SCRIPT VARS "PRIVATE"
        self.tick_timer: float = 0.0

    @abstractmethod
    def action(self) -> None:
        pass

    def process(self, delta: float) -> None:
        # update lifetime
        self.lifetime -= delta
        if self.lifetime <= 0.0:
            self.deactivate()
            return
        # update tick timer
        self.tick_timer -= delta
        if self.tick_timer <= 0.0: # TODO take into account <= 0.0 value ? (get abs)
            self.action()

    def activate(self) -> bool:
        # TODO add effect stacking ? + refreshing
        if self.target.has_effect(self): return False # check if effect already exists
        self.target.add_effect(self)
        self.action()
        return True

    def deactivate(self) -> None:
        self.target.remove_effect(self)

    def reset_timer(self) -> None:
        self.tick_timer = self.tick_delay


if __name__ == '__main__':
    pass
