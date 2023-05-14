from __future__ import annotations
import numpy as np

from src.game.main.entities.entity import Entity
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.interfaces.collidable import Collidable
from src.game.main.singletons.collision_handler import CollisionHandler


class CollidableEntity(Entity, Collidable):

    def __init__(self, sprite_url: str, mass: float, belongs_to: ObjectCategory, collides_with: list[ObjectCategory]) -> None:
        Entity.__init__(self, sprite_url=sprite_url)
        Collidable.__init__(self, belongs_to, collides_with)
        self.mass: float = mass

    def on_update(self, delta_time: float = 1 / 60) -> None:
        super(CollidableEntity, self).on_update(delta_time)
        # move itself
        self.position = (self.position[0] + self.velocity[0] * delta_time, self.position[1] + self.velocity[1] * delta_time)
        self.handle_collisions(delta_time)

    def handle_collisions(self, delta: float) -> list[Collidable]:
        collisions: list[Collidable] = CollisionHandler.check_collision(self)
        for collider in collisions:
            if collider.belongs_to != ObjectCategory.PROJECTILES:
                collision_vector = CollisionHandler.get_collision_vector(self, collider)

                if collision_vector is None:
                    pass
                else:
                    stop_direction = collision_vector/np.linalg.norm(collision_vector)

                    # Calculate the component of the velocity vector in the stop direction
                    velocity_component = np.dot(self.velocity, stop_direction)

                    # Calculate the projection of the velocity vector onto the stop direction
                    velocity_projection = stop_direction * velocity_component

                    # force that pushes away from the colliding object only if we are inside it's hitbox
                    force = np.array(self.position) - np.array(collider.position)
                    force = force/np.linalg.norm(force)

                    # Subtract the projection from the original velocity vector to stop the ship's movement in the stop_direction
                    # push_vector = force * Config.Constants.get("COLLISION_FORCE") * delta
                    # if collider.belongs_to != ObjectCategory.STATIC:
                    #     push_vector *= collider.mass / self.mass
                    # self.velocity -= velocity_projection - push_vector
                    # self.velocity = clamp(self.velocity, 0.0, min(magnitude(self.velocity)*2, 1000.0))

                    # NOTE: Different approach
                    if collider.belongs_to == ObjectCategory.STATIC:
                        relative_vel = -1 * np.array(self.velocity)
                    else:
                        relative_vel = np.array(collider.velocity) - np.array(self.velocity)


                    if collider.belongs_to == ObjectCategory.STATIC:
                        impulse_magnitude = -(2.5) * np.dot(relative_vel, stop_direction) / (1.0 / 10000.0 + 1.0 / self.mass)
                    else:
                        impulse_magnitude = -(2.5) * np.dot(relative_vel, stop_direction) / (1.0 / collider.mass + 1.0 / self.mass)
                    impulse_vector = stop_direction * impulse_magnitude * delta

                    self.velocity -= impulse_vector
                    if collider.belongs_to != ObjectCategory.STATIC:
                        collider.velocity += impulse_vector

        return collisions
