
import arcade
import numpy as np
from typing import Tuple
from src.auxilary.LinearMovement import LinearMovement
from src.auxilary.MovementType import MovementType
from src.auxilary.ObjectCategory import ObjectCategory
from src.entities.Entity import Entity
from src.interfaces.Collidable import Collidable
from src.interfaces.Destroyable import Destroyable
from src.interfaces.Launchable import Launchable
from src.singletons.CollisionHandler import CollisionHandler
from src.util.VectorMath import normalize, length


class Projectile(Entity, Launchable, Collidable, Destroyable):

    def __init__(self, sprite_url: str, belongs_to: list[ObjectCategory], collides_with: list[ObjectCategory],
                 damage: float = 10, acceleration: float = 0.0, lifetime: float = 2.0,
                 falloff_damage: list[Tuple[float, float]] = None, penetrations: int = 1, bounces: int = 0,
                 movement_type: MovementType = None) -> None:
        Entity.__init__(self, sprite_url)
        Collidable.__init__(self, belongs_to, collides_with)
        self.damage: float = damage
        self.acceleration: float = acceleration
        self.lifetime: float = lifetime
        self.falloff_damage: list[Tuple[float, float]] = falloff_damage
        self.penetrations: int = penetrations
        self.bounces: int = bounces
        self.movement_type: MovementType = LinearMovement() if movement_type is None else movement_type


    def on_update(self, delta_time: float = 1 / 60) -> None:
        # lifetime update
        self.lifetime -= delta_time
        if self.lifetime <= 0.0: # stop immediately
            self.destroy(); return
        # acceleration update
        direction: arcade.Vector = normalize(self.velocity)
        if self.acceleration < 0.0 and length(self.velocity) <= 1.2 * -self.acceleration * delta_time:
            self.velocity = (0.0, 0.0) # stop if at low speed nad decelerating
        else:
            acceleration_vector = (direction[0]*self.acceleration*delta_time, direction[1]*self.acceleration*delta_time)
            self.velocity = (self.velocity[0]+acceleration_vector[0], self.velocity[1]+acceleration_vector[1])
        self.movement_type.move(delta_time, self)
        # check collisions
        # TODO temporary setup
        # TODO add damage dealt at collision detection
        hit_list = CollisionHandler.check_collision(self)
        if hit_list: self.destroy()


    def launch(self, from_: arcade.Point, angle: float, speed: float) -> None:
        direction: arcade.Vector = (np.cos(np.deg2rad(angle)), np.sin(np.deg2rad(angle))) # already normalized
        self.position = from_
        self.angle = angle
        self.velocity = (direction[0] * speed, direction[1] * speed)


    def destroy(self) -> Destroyable:
        self.kill()
        return self


if __name__ == '__main__':
    pass
