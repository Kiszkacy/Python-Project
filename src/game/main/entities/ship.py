
import arcade
import numpy as np

from src.game.main.entities.structure import Structure
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.util.math import normalize, clamp, magnitude
from src.game.main.weapons.launchable_gun import LaunchableGun
from src.game.main.weapons.weapon import Weapon


class Ship(Structure):

    def __init__(self, sprite_url: str, mass: float, belongs_to: ObjectCategory, collides_with: list[ObjectCategory],
                 hp_max: float = 100.0, shd_max: float = 25.0, power_max: float = 100.0, power_regen_amount: float = 25.0,
                 power_regen_delay: float = 2.5, rotation_speed: float = 300.0, max_speed: float = 550.0,
                 acceleration: float = 750.0, deceleration: float = 50.0, weapons: list[Weapon] = None,
                 weapon_count: int = 1) -> None:
        Structure.__init__(self, sprite_url, mass, belongs_to, collides_with, hp_max, shd_max, power_max, power_regen_amount, power_regen_delay)
        self.rotation_speed: float = rotation_speed
        self.max_speed: float = max_speed
        self.acceleration: float = acceleration
        self.deceleration: float = deceleration
        self.weapons: list[Weapon] = [Weapon(LaunchableGun())] if weapons is None else weapons
        self.weapon_count: int = weapon_count
        # SCRIPT VARS "PRIVATE"
        self.weapon_idx: int = 0
        self.is_flying: bool = False

    def on_update(self, delta_time: float = 1 / 60) -> None:
        super(Ship, self).on_update(delta_time)
        # decelerate
        if not self.is_flying:
            if magnitude(self.velocity) >= 1.2*self.deceleration*delta_time: # TODO hardcoded move to global const or something
                direction: arcade.Vector = normalize(self.velocity)
                self.velocity = (self.velocity[0] - direction[0]*self.deceleration*delta_time, self.velocity[1] - direction[1]*self.deceleration*delta_time)
            else:
                self.velocity = (0.0, 0.0)
        # update weapons
        for weapon in self.weapons:
            weapon.process(delta_time)
        # update is_flying check
        self.is_flying = False

    def fly(self, delta: float) -> None:
        self.is_flying = True
        direction: arcade.Vector = (np.cos(np.deg2rad(self.angle)), np.sin(np.deg2rad(self.angle))) # already normalized
        acceleration_vector: arcade.Vector = (direction[0]*self.acceleration, direction[1]*self.acceleration)
        self.velocity = (self.velocity[0] + acceleration_vector[0]*delta, self.velocity[1] + acceleration_vector[1]*delta)
        self.velocity = clamp(self.velocity, 0.0, self.max_speed)

    def rotate_towards(self, delta: float, target_angle_radians: float) -> None:
        target_angle_rad: float = target_angle_radians

        if target_angle_rad < 0.0: target_angle_rad += 2 * np.pi
        angle_rad: float = np.deg2rad(self.angle)
        rotation_rad: float = np.deg2rad(self.rotation_speed)
        angle_rad_diff: float = target_angle_rad - angle_rad
        # rotation clockwise or anticlockwise?
        clockwise: bool = False
        if abs(angle_rad_diff) <= rotation_rad * delta:
            # jump to target angle if small
            angle_rad = target_angle_rad
        elif angle_rad_diff > 0 and abs(angle_rad_diff) >= np.pi:
            clockwise = True
        elif angle_rad_diff < 0 and abs(angle_rad_diff) < np.pi:
            clockwise = True

        if angle_rad != target_angle_rad and clockwise:
            angle_rad -= rotation_rad * delta
        elif angle_rad != target_angle_rad:
            angle_rad += rotation_rad * delta

        if angle_rad > 2 * np.pi:
            angle_rad -= 2 * np.pi
        elif angle_rad < 0:
            angle_rad += 2 * np.pi

        self.angle = np.degrees(angle_rad)

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


if __name__ == '__main__':
    pass
