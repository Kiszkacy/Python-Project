
import arcade
import numpy as np
from src.auxilary.LinearMovement import LinearMovement
from src.auxilary.MovementType import MovementType
from src.entities.Entity import Entity
from src.util.VectorMath import normalize, length
from src.weapons.LaunchableGun import LaunchableGun
from src.weapons.Weapon import Weapon
from src.singletons.CollisionHandler import CollisionHandler
from src.interfaces.Collidable import Collidable
from src.auxilary.ObjectCategory import ObjectCategory



class Ship(Entity, Collidable):
    # TODO move this to config file
    POWER_TICKS_PER_SECOND: int = 4
    POWER_REGEN_COOLDOWN: float = 1.0 / POWER_TICKS_PER_SECOND

    def __init__(self, sprite_url: str, belongs_to: ObjectCategory, collides_with: list[ObjectCategory],
                 rotation_speed: float = 300.0, max_speed: float = 550.0,
                 acceleration: float = 750.0, deceleration: float = 50.0, weapons: list[Weapon] = None,
                 weapon_count: int = 1, power_max: float = 100.0, power_regen_amount: float = 25.0,
                 power_regen_delay: float = 2.5,  movement_type: MovementType = None) -> None:
        Entity.__init__(self, sprite_url=sprite_url)
        Collidable.__init__(self, belongs_to, collides_with)
        self.rotation_speed: float = rotation_speed
        self.max_speed: float = max_speed
        self.acceleration: float = acceleration
        self.deceleration: float = deceleration
        self.weapons: list[Weapon] = [Weapon(LaunchableGun())] if weapons is None else weapons
        self.weapon_count: int = weapon_count
        self.power_max: float = power_max
        self.power_regen_amount: float = power_regen_amount
        self.power_regen_delay: float = power_regen_delay
        self.movement_type: MovementType = LinearMovement() if movement_type is None else movement_type
        # SCRIPT VARS "PRIVATE"
        self.power: float = self.power_max # PLEASE US SETTER ON ME THANKS
        self.power_timer: float = 0.0
        self.power_regenerating: bool = False
        self.power_timer_online: bool = False
        self.weapon_idx: int = 0


    def on_update(self, delta_time: float = 1 / 60) -> None:
        super(Ship, self).on_update(delta_time)
        self.movement_type.move(delta_time, self)
        self.handle_collision()
        # decelerate
        if length(self.velocity) >= 1.2*self.deceleration*delta_time: # TODO hardcoded move to global const or something
            direction: arcade.Vector = normalize(self.velocity)
            self.velocity = (self.velocity[0] - direction[0]*self.deceleration*delta_time, self.velocity[1] - direction[1]*self.deceleration*delta_time)
        else:
            self.velocity = (0.0, 0.0)
        # update power timer
        if self.power_timer_online:
            self.power_timer -= delta_time
            if self.power_timer <= 0.0:
                self.power_regen()
        # update weapons
        for weapon in self.weapons:
            weapon.process(delta_time)


    def fly(self, delta: float) -> None:
        direction: arcade.Vector = (np.cos(np.deg2rad(self.angle)), np.sin(np.deg2rad(self.angle))) # already normalized
        acceleration_vector: arcade.Vector = (direction[0]*self.acceleration, direction[1]*self.acceleration)
        self.velocity = (self.velocity[0] + acceleration_vector[0]*delta, self.velocity[1] + acceleration_vector[1]*delta)


    def fire(self) -> None:
        # TODO weird angle offset | PLEASE CHECK DEFAULT SPRITE ANGLES
        if self.weapons[self.weapon_idx].fire(self.position, self.angle, self.power):
            self.set_power(self.power - self.weapons[self.weapon_idx].main_gun.power_cost)


    def altfire(self) -> None:
        # TODO weird angle offset | PLEASE CHECK DEFAULT SPRITE ANGLES
        if self.weapons[self.weapon_idx].altfire(self.position, self.angle, self.power):
            self.set_power(self.power - self.weapons[self.weapon_idx].alt_gun.power_cost)


    def switch_weapon(self, idx: int) -> bool:
        if self.weapon_count <= idx: return False
        self.weapon_idx = idx
        return True


    def power_regen(self) -> None:
        if self.power >= self.power_max: # stop when at max power
            self.power_regenerating = False
            self.power_timer_online = False
            return
        self.power_regenerating = True
        self.power = min(self.power_max, self.power + self.power_regen_amount * Ship.POWER_REGEN_COOLDOWN)
        self.power_timer = Ship.POWER_REGEN_COOLDOWN


    def power_regen_request(self) -> None:
        self.power_timer_online = True
        self.power_regenerating = False
        self.power_timer = self.power_regen_delay


    def set_power(self, to: float) -> None:
        if to < self.power:
            self.power_regen_request()
        self.power = max(min(to, self.power_max), 0.0)

    def handle_collision(self):
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
                    self.velocity -= velocity_projection - force*25  # TODO remove the constant


if __name__ == '__main__':
    pass
