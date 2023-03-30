
import arcade
from src.interfaces.Launchable import Launchable
from src.interfaces.Processable import Processable


class Gun(Processable):

    def __init__(self, damage: float = 3.0, power_cost: float = 2.0, barrel_count: int = 1,
                 barrels: list[arcade.Point] = None, barrels_even_offset: float = 3.0) -> None:
        self.damage: float = damage
        self.power_cost: float = power_cost
        self.barrel_count: int = barrel_count
        self.barrels_even_offset: float = barrels_even_offset
        self.barrels: list[arcade.Point]
        if barrels is not None: self.barrels = barrels
        elif barrel_count == 1: self.barrels = [(0.0, 0.0)]
        else:                   self.barrels = [(-barrels_even_offset/2.0 + i*barrels_even_offset/(barrel_count-1), 0.0) for i in range(barrel_count)]
        # SCRIPT VARS "PRIVATE"
        self.is_shooting: bool = False
        self.cd: float = 0.0


    def process(self, delta: float) -> None:
        self.cd -= delta


    # TODO self.is_shooting is currently pointless
    # TODO (requires Input class to be processed always before this to work properly in the future)
    def shoot(self, from_: arcade.Point, angle: float) -> None:
        pass


    def stop_shoot(self) -> None:
        self.is_shooting = False


    def can_shoot(self, power: float) -> bool:
        return power > self.power_cost and self.cd <= 0.0


if __name__ == '__main__':
    pass
