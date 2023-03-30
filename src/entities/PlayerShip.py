
import arcade
import numpy as np
from src.entities.Ship import Ship
from src.singletons.InputHandler import InputHandler
from src.tempclasses.tempWeapon import TempWeapon
from src.weapons.Weapon import Weapon


class PlayerShip(Ship): # TODO

    def __init__(self) -> None:
        super().__init__(sprite_url="..\\resources\\sprites\\tmp.png")
        self.position = (1280/2, 720/2) # TODO hardcoded values | (sprite position parameter <=> (center_x, center_y)
        self.weapon: Weapon = TempWeapon() # TODO hardcoded


    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.process_input(delta_time)
        self.rotate_towards_mouse(delta_time)
        # update all not sprite children
        self.weapon.process(delta_time)


    def process_input(self, delta: float) -> None:
        if InputHandler.key_pressed[arcade.key.SPACE]:
            self.weapon.fire(self.position, (180.0+self.angle) % 360, 100.0) # TODO hardcoded power | ALSO PLEASE CHECK DEFAULT ANGLE FOR SPRITES


    def rotate_towards_mouse(self, delta: float) -> None: # TODO add interpolation when Ship is ready
        mouse: arcade.Point = InputHandler.mouse

        x_diff: float = self.position[0] - mouse[0]
        y_diff: float = self.position[1] - mouse[1]
        angle: float = np.arctan2(y_diff, x_diff)
        if angle < 0.0: angle += 2 * np.pi

        self.angle = np.degrees(angle)



if __name__ == '__main__':
    pass
