
import arcade
import numpy as np

from src.game.main.entities.object import Object
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.interfaces.collidable import Collidable
from src.game.main.interfaces.destroyable import Destroyable
from src.game.main.util.math import magnitude


class Asteroid(Object):

    ROTATION_SPEED_RATIO: float = 100.0
    ROTATION_SPEED: float = 5.0 # in deg

    def __init__(self, sprite_url: str, mass: float, hp_max: float, starting_velocity: arcade.Vector, starting_position: arcade.Point,
                 belongs_to: ObjectCategory = ObjectCategory.NEUTRAL, collides_with: list[ObjectCategory] = None) -> None:

        if collides_with is None: collides_with = [ObjectCategory.STATIC, ObjectCategory.ENEMIES, ObjectCategory.PLAYER, ObjectCategory.NEUTRAL]
        super(Asteroid, self).__init__(sprite_url, mass, belongs_to, collides_with, hp_max, shd_max=0.0)
        self.velocity = starting_velocity
        self.angle_rot: float = (magnitude(starting_velocity) / Asteroid.ROTATION_SPEED_RATIO) * Asteroid.ROTATION_SPEED
        self.angle_dir: float = np.random.randint(0, 2) * 2 - 1 # -1 or 1
        self.position = starting_position

    def on_update(self, delta_time: float = 1 / 60) -> None:
        super(Asteroid, self).on_update(delta_time)
        # rotate
        self.angle += self.angle_rot * self.angle_dir

    def handle_collisions(self, delta: float) -> list[Collidable]:
        collisions: list[Collidable] = super(Asteroid, self).handle_collisions(delta)

        if collisions: # update rotation param
            self.angle_rot = (magnitude(self.velocity) / Asteroid.ROTATION_SPEED_RATIO) * Asteroid.ROTATION_SPEED
            self.angle_dir: float = np.random.randint(0, 2) * 2 - 1 # -1 or 1

        return collisions

    def damage(self, amount: float) -> float:
        dealt: float = super(Asteroid, self).damage(amount)
        if self.hp <= 0.0 and dealt != 0.0:
            self.destroy()
        return dealt

    def destroy(self) -> Destroyable:
        self.kill()
        return self


if __name__ == '__main__':
    pass