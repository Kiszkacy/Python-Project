
import arcade
import numpy as np
from src.auxilary.ObjectCategory import ObjectCategory
from src.entities.Entity import Entity
from src.interfaces.Collidable import Collidable
from src.interfaces.Damageable import Damageable
from src.interfaces.Destroyable import Destroyable
from src.singletons.CollisionHandler import CollisionHandler
from src.util.VectorMath import length


class Asteroid(Entity, Collidable, Damageable, Destroyable):

    ROTATION_SPEED_RATIO: float = 100.0
    ROTATION_SPEED: float = 5.0 # in deg

    def __init__(self, sprite_url: str, belongs_to: ObjectCategory, collides_with: list[ObjectCategory], hp_max: float,
                 starting_velocity: arcade.Vector, starting_position: arcade.Point) -> None:
        Entity.__init__(self, sprite_url=sprite_url)
        Collidable.__init__(self, belongs_to, collides_with)
        Damageable.__init__(self, hp_max, shd_max=0)
        self.velocity = starting_velocity
        self.angle_rot: float = (length(starting_velocity) / Asteroid.ROTATION_SPEED_RATIO) * Asteroid.ROTATION_SPEED
        self.angle_dir: float = np.random.randint(0, 2) * 2 - 1 # -1 or 1
        self.position = starting_position


    def on_update(self, delta_time: float = 1 / 60) -> None:
        # just move
        self.position = (self.position[0] + self.velocity[0] * delta_time, self.position[1] + self.velocity[1] * delta_time)
        # rotate
        self.angle += self.angle_rot * self.angle_dir
        # collisions
        self.handle_collision(delta_time)


    def handle_collision(self, delta: float) -> None:
        collisions: list[arcade.Sprite | Collidable] = CollisionHandler.check_collision(self)
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

        if collisions: # update rotation param
            self.angle_rot = (length(self.velocity) / Asteroid.ROTATION_SPEED_RATIO) * Asteroid.ROTATION_SPEED
            self.angle_dir: float = np.random.randint(0, 2) * 2 - 1 # -1 or 1


    def damage(self, amount: float) -> float:
        dealt: float = super(Asteroid, self).damage(amount)
        if self.hp <= 0.0:
            self.destroy()
        return dealt


    def destroy(self) -> Destroyable:
        self.kill()
        return self