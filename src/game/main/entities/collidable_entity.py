from __future__ import annotations

from typing import List

import numpy as np

from src.game.main.entities.entity import Entity
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.interfaces.bucketable import Bucketable
from src.game.main.interfaces.collidable import Collidable
from src.game.main.singletons.collision_handler import CollisionHandler
from src.game.main.singletons.config import Config
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.util.math import clamp, magnitude


class CollidableEntity(Entity, Collidable, Bucketable):

    def __init__(self, sprite_url: str, mass: float, belongs_to: ObjectCategory, collides_with: list[ObjectCategory]) -> None:
        Entity.__init__(self, sprite_url=sprite_url)
        Collidable.__init__(self, belongs_to, collides_with)
        self.mass: float = mass
        self.bucket_x_idx: int = 0
        self.bucket_y_idx: int = 0


    def on_update(self, delta_time: float = 1 / 60) -> None:
        super(CollidableEntity, self).on_update(delta_time)
        # move itself
        self.position = (self.position[0] + self.velocity[0] * delta_time, self.position[1] + self.velocity[1] * delta_time)
        self.update_bucket_position()
        self.handle_collisions(delta_time)


    def update_bucket_position(self) -> None:
        bs: int = Config.Constants.get("BUCKET_SIZE")
        bucket_x: int = int(self.position[0] // bs)
        bucket_y: int = int(self.position[1] // bs)
        if bucket_x != self.bucket_x_idx or bucket_y != self.bucket_y_idx:
            self.remove_from_sprite_lists()
            if not EntityHandler.add(self, self.belongs_to, True): # was not added -> moved out of bounds
                self.out_of_bounds()


    def out_of_bounds(self) -> None:
        self.kill()


    def handle_collisions(self, delta: float) -> List[Collidable]:
        collisions: list[Collidable] = CollisionHandler.check_collision(self, True)
        return self.collision_resolution(delta, collisions)


    def collision_resolution(self, delta: float, collisions: List[Collidable]) -> List[Collidable]:
        for collider in collisions:
            if collider.belongs_to == ObjectCategory.PROJECTILES: continue
            collision_vector = CollisionHandler.get_collision_vector(self, collider)

            if collision_vector is None: continue

            stop_direction = collision_vector / np.linalg.norm(collision_vector)

            # Calculate the component of the velocity vector in the stop direction
            our_velocity_component = np.dot(self.velocity, stop_direction)

            max_mass: float = Config.Constants.get("MAX_MASS")

            if collider.belongs_to == ObjectCategory.STATIC or collider.mass >= max_mass:
                their_velocity_component = 0
            else:
                their_velocity_component = np.dot(collider.velocity, -stop_direction)

            # relative speed between us, nad collider
            relative_speed = abs(our_velocity_component - their_velocity_component)

            # Calculate the projection of the velocity vector onto the stop direction
            velocity_projection = stop_direction * relative_speed * collider.mass / self.mass * delta

            # this cases asteroids to have 4-d velocity?
            # velocity_projection = clamp(velocity_projection * Config.Constants.get("COLLISION_FORCE"), 0, 400)
            if collider.belongs_to == ObjectCategory.STATIC or collider.mass >= max_mass:
                # velocity_projection /= collider.mass/self.mass
                pass

            if self.belongs_to == ObjectCategory.STATIC or self.mass >= max_mass:
                pass
            elif collider.belongs_to == ObjectCategory.STATIC or collider.mass >= max_mass:
                shift = np.array(collider.position) - self.position
                shift /= np.linalg.norm(shift)
                if np.dot(shift, stop_direction):
                    self.velocity -= np.array(self.velocity)*2
            else:
                self.velocity += velocity_projection * Config.Constants.get("COLLISION_FORCE")

            # self.velocity = clamp(self.velocity, 0.0, min(magnitude(self.velocity), 1000.0))

        return collisions
