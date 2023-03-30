
from typing import Optional
from src.interfaces.Processable import Processable
from src.weapons.Gun import Gun
import arcade


class Weapon(Processable):

    def __init__(self, main_gun: Gun, alt_gun: Optional[Gun] = None) -> None:
        self.main_gun: Gun = main_gun
        self.alt_gun: Optional[Gun] = alt_gun


    def process(self, delta: float) -> None:
        self.main_gun.process(delta)
        if self.alt_gun is not None:
            self.alt_gun.process(delta)


    def fire(self, from_: arcade.Point, angle: float, power: float) -> bool:
        if not self.main_gun.can_shoot(power):
            return False

        self.main_gun.shoot(from_, angle)
        return True


    def altfire(self, from_: arcade.Point, angle: float, power: float) -> float:
        if self.alt_gun is None or not self.alt_gun.can_shoot(power):
            return False

        self.alt_gun.shoot(from_, angle)
        return True



if __name__ == '__main__':
    pass
