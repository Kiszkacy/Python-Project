import arcade
import numpy as np

from src.game.main.entities.entity import Entity
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.interfaces.collidable import Collidable
from src.game.main.interfaces.damageable import Damageable
from src.game.main.interfaces.destroyable import Destroyable
from src.game.main.singletons.collision_handler import CollisionHandler


class Object(Entity, Collidable, Damageable, Destroyable):

    def __init__(self, sprite_url: str, mass: float, belongs_to: ObjectCategory, collides_with: list[ObjectCategory],
                 hp_max: float, shd_max: float) -> None:
        Entity.__init__(self, sprite_url=sprite_url)
        Collidable.__init__(self, belongs_to, collides_with)
        Damageable.__init__(self, hp_max, shd_max)
        self.mass: float = mass

    def on_update(self, delta_time: float = 1 / 60) -> None:
        super(Object, self).on_update(delta_time)
        # move itself
        self.position = (self.position[0] + self.velocity[0] * delta_time, self.position[1] + self.velocity[1] * delta_time)
        self.handle_collisions(delta_time)
        # update shield timer
        if self.shield_timer_online:
            self.shield_timer -= delta_time
            if self.shield_timer <= 0.0:
                self.shield_regen()

    def damage(self, amount: float) -> float:
        dealt: float = super(Object, self).damage(amount)
        if self.hp <= 0.0:
            self.destroy()
        return dealt

    def destroy(self) -> Destroyable:
        self.kill()
        return self

    def handle_collisions(self, delta: float) -> list[Collidable]:
        collisions: list[Collidable] = CollisionHandler.check_collision(self)
        for collision in collisions:
            if collision.belongs_to != ObjectCategory.PROJECTILES:
                collision_vector = CollisionHandler.get_collision_vector(self, collision)

                if collision_vector is None:
                    pass
                else:
                    stop_direction = collision_vector/np.linalg.norm(collision_vector)

                    # Calculate the component of the velocity vector in the stop direction
                    velocity_component = np.dot(self.velocity, stop_direction)

                    # Calculate the projection of the velocity vector onto the stop direction
                    velocity_projection = stop_direction * velocity_component

                    # force that pushes away from the colliding object only if we are inside it's hitbox
                    force = np.array(self.position) - np.array(collision.position)
                    force = force/np.linalg.norm(force)

                    # Subtract the projection from the original velocity vector to stop the ship's movement in the stop_direction
                    self.velocity -= velocity_projection - force * 2500.0 * delta  # TODO remove the constant

        return collisions
