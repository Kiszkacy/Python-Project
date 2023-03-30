
import arcade
import numpy as np
from src.entities.Entity import Entity
from src.interfaces.Launchable import Launchable


class Projectile(Entity, Launchable):

    def __init__(self, sprite_url: str) -> None:
        super().__init__(sprite_url)


    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.position = (self.position[0] + self.velocity[0] * delta_time, self.position[1] + self.velocity[1] * delta_time)
        # pass


    def launch(self, from_: arcade.Point, angle: float, speed: float) -> None:
        direction: arcade.Vector = (np.cos(np.deg2rad(angle)), np.sin(np.deg2rad(angle))) # already normalized
        self.position = from_
        self.angle = angle
        self.velocity[0] = direction[0] * speed
        self.velocity[1] = direction[1] * speed



if __name__ == '__main__':
    pass
