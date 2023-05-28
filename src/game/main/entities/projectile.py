
import arcade
import numpy as np
from typing import Tuple

from src.game.main.entities.entity import Entity
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.events.damage_event import DamageEvent
from src.game.main.events.destroy_event import DestroyEvent
from src.game.main.interfaces.collidable import Collidable
from src.game.main.interfaces.damageable import Damageable
from src.game.main.interfaces.destroyable import Destroyable
from src.game.main.interfaces.launchable import Launchable
from src.game.main.movement.linear_movement import LinearMovement
from src.game.main.movement.movement_type import MovementType
from src.game.main.singletons.collision_handler import CollisionHandler
from src.game.main.singletons.event_register import EventRegister
from src.game.main.util.math import normalize, magnitude
from src.game.main.util.path_loader import get_absolute_resource_path


class Projectile(Entity, Launchable, Collidable, Destroyable):

    def __init__(self, sprite_url: str = get_absolute_resource_path("\\sprites\\error.png"),
                 damage: float = 10, acceleration: float = 0.0, lifetime: float = 2.0,
                 falloff_damage: list[Tuple[float, float]] = None, penetrations: int = 1, bounces: int = 0,
                 movement_type: MovementType = None, belongs_to: ObjectCategory = ObjectCategory.PROJECTILES,
                 collides_with: list[ObjectCategory] = None) -> None:

        if collides_with is None: collides_with = [ObjectCategory.STATIC, ObjectCategory.ENEMIES, ObjectCategory.NEUTRAL]
        Entity.__init__(self, sprite_url)
        Collidable.__init__(self, belongs_to, collides_with)
        self.damage: float = damage
        self.acceleration: float = acceleration
        self.lifetime: float = lifetime
        self.falloff_damage: list[Tuple[float, float]] = falloff_damage # TODO not implemented
        self.penetrations: int = penetrations
        self.bounces: int = bounces # TODO not implemented
        self.movement_type: MovementType = LinearMovement() if movement_type is None else movement_type
        # SCRIPT VARS "PRIVATE"
        self.colliding_with: list[Collidable] = []

    def on_update(self, delta_time: float = 1 / 60) -> None:
        # lifetime update
        self.lifetime -= delta_time
        if self.lifetime <= 0.0: # stop immediately
            self.destroy(); return
        # movement update
        self.movement_update(delta_time)
        # check collisions
        self.handle_collisions()

    def movement_update(self, delta: float) -> None:
        # acceleration update
        direction: arcade.Vector = normalize(self.velocity)
        if self.acceleration < 0.0 and magnitude(self.velocity) <= 1.2 * -self.acceleration * delta: # TODO ALSO HARDCODED
            self.velocity = (0.0, 0.0)  # stop if at low speed nad decelerating
        else:
            acceleration_vector = (direction[0] * self.acceleration * delta, direction[1] * self.acceleration * delta)
            self.velocity = (self.velocity[0] + acceleration_vector[0], self.velocity[1] + acceleration_vector[1])
        # move
        self.movement_type.move(delta, self)

    def launch(self, from_: arcade.Point, angle: float, speed: float) -> None:
        direction: arcade.Vector = (np.cos(np.deg2rad(angle)), np.sin(np.deg2rad(angle))) # already normalized
        self.position = from_
        self.angle = angle
        self.velocity = (direction[0] * speed, direction[1] * speed)

    def destroy(self) -> Destroyable:
        self.kill()
        EventRegister.register_new(DestroyEvent(self))
        return self

    def handle_collisions(self) -> None:
        colliders: list[Collidable] = CollisionHandler.check_collision(self, True)
        if colliders is []: return

        for i in range(len(self.colliding_with) - 1, -1, -1):
            if self.colliding_with[i] in colliders:
                colliders.remove(self.colliding_with[i])
            else:
                self.colliding_with.pop(i)

        for c in colliders:
            self.penetrations -= 1
            if isinstance(c, Damageable): # TODO this might not be needed?
                damage_dealt: float = c.damage(self.damage)
                EventRegister.register_new(DamageEvent(c, damage_dealt, self))
            if self.penetrations == 0:
                self.destroy()
                break


if __name__ == '__main__':
    pass
