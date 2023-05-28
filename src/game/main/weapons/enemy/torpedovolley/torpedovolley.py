import copy

import numpy as np

from src.game.main.effects.active.damage_effect import DamageEffect
from src.game.main.entities.projectile import Projectile
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.events.damage_event import DamageEvent
from src.game.main.interfaces.affectable import Affectable
from src.game.main.interfaces.collidable import Collidable
from src.game.main.interfaces.damageable import Damageable
from src.game.main.movement.sinusoidal_movement import SinusoidalMovement
from src.game.main.singletons.collision_handler import CollisionHandler
from src.game.main.singletons.event_register import EventRegister
from src.game.main.util.path_loader import get_absolute_resource_path
from src.game.main.weapons.launchable_gun import LaunchableGun
from src.game.main.weapons.weapon import Weapon


class ProjectileTorpedoVolley(Projectile):

    def __init__(self) -> None:
        Projectile.__init__(self, sprite_url=get_absolute_resource_path("\\sprites\\projectiles\\big_005.png"),
                            collides_with=[ObjectCategory.PLAYER, ObjectCategory.NEUTRAL, ObjectCategory.STATIC],
                            damage=10, lifetime=1.5, acceleration=750.0)

    def handle_collisions(self) -> None: # TODO code repetition
        colliders: list[Collidable] = CollisionHandler.check_collision(self, True)
        if colliders is []: return

        for i in range(len(self.colliding_with) - 1, -1, -1):
            if self.colliding_with[i] in colliders:
                colliders.remove(self.colliding_with[i])
            else:
                self.colliding_with.pop(i)

        for c in colliders:
            self.penetrations -= 1
            if isinstance(c, Damageable):  # TODO this might not be needed?
                damage_dealt: float = c.damage(self.damage)
                EventRegister.register_new(DamageEvent(c, damage_dealt, self))
                if isinstance(c, Affectable) and not c.has_effect(DamageEffect):
                    c.add_effect(DamageEffect(c, 5.0, 1.0, 2))
            if self.penetrations == 0:
                self.destroy()
                break


class GunTorpedoVolley(LaunchableGun):

    def __init__(self) -> None:
        super().__init__(launchable=ProjectileTorpedoVolley(), launch_speed=50.0, shots_per_sec=0.5, barrel_count=3, even_spread=90.0)


class WeaponTorpedoVolley(Weapon):

    def __init__(self) -> None:
        super(WeaponTorpedoVolley, self).__init__(GunTorpedoVolley())


if __name__ == '__main__':
    pass
