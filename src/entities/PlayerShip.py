
import arcade
import numpy as np
from src.entities.Ship import Ship
from src.singletons.InputHandler import InputHandler
from src.weapons.aura.WeaponAura import WeaponAura
from src.weapons.basic.WeaponBasic import WeaponBasic
from src.weapons.shotgun.WeaponShotgun import WeaponShotgun
from src.weapons.sinus.WeaponSinus import WeaponSinus
from src.weapons.weird.WeaponWeird import WeaponWeird
from src.auxilary.ObjectCategory import ObjectCategory


class PlayerShip(Ship): # TODO

    def __init__(self, starting_position: arcade.Point) -> None:
        super().__init__(sprite_url="..\\resources\\sprites\\tmp_ship0.png",
                         weapons=[WeaponBasic(ObjectCategory.PLAYER), WeaponShotgun(), WeaponAura(), WeaponSinus(), WeaponWeird()],
                         weapon_count=5,
                         belongs_to=ObjectCategory.PLAYER,
                         collides_with=[ObjectCategory.STATIC, ObjectCategory.ENEMIES, ObjectCategory.PROJECTILES])
        self.position = starting_position


    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.process_input(delta_time)
        self.rotate_towards_mouse(delta_time)
        super(PlayerShip, self).on_update()


    def process_input(self, delta: float) -> None:
        if InputHandler.key_binding_pressed("SHOOT"): # TODO switch to mouse
            self.fire()
        if InputHandler.key_binding_pressed("ALTFIRE"): # TODO switch to mouse
            self.altfire()
        if InputHandler.key_binding_pressed("FLY"):
            self.fly(delta)
        if InputHandler.key_binding_pressed("WEAPON0"):
            self.switch_weapon(0)
        if InputHandler.key_binding_pressed("WEAPON1"):
            self.switch_weapon(1)
        if InputHandler.key_binding_pressed("WEAPON2"):
            self.switch_weapon(2)
        if InputHandler.key_binding_pressed("WEAPON3"):
            self.switch_weapon(3)
        if InputHandler.key_binding_pressed("WEAPON4"):
            self.switch_weapon(4)


    def rotate_towards_mouse(self, delta: float) -> None: # TODO add interpolation when Ship is ready
        mouse: arcade.Point = InputHandler.mouse

        x_diff: float = mouse[0] - self.position[0]
        y_diff: float = mouse[1] - self.position[1]
        target_angle_rad: float = np.arctan2(y_diff, x_diff)
        self.rotate_towards(delta, target_angle_rad)


if __name__ == '__main__':
    pass
