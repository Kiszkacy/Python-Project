from copy import deepcopy
from typing import Optional

import arcade
import numpy as np
import pytest

from src.game.main.entities.entity import Entity
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.interfaces.launchable import Launchable
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.weapons.launchable_gun import LaunchableGun
from src.game.main.weapons.weapon import Weapon


class TestGun(LaunchableGun):
    def register_launchable(self, instance: Launchable) -> None:
        EntityHandler.add(instance, instance.belongs_to, False)


@pytest.mark.randomize(ncalls=1)
def test_fire():
    EntityHandler.categorized[ObjectCategory.PROJECTILES].clear()
    gun: LaunchableGun = TestGun()
    weapon: Weapon = Weapon(gun)

    weapon.fire((0.0, 0.0), 0.0, np.inf)

    assert len(EntityHandler.categorized[ObjectCategory.PROJECTILES]) != 0, "Weapon fire does not work properly. No instance created."


@pytest.mark.randomize(ncalls=1)
def test_altfire():
    EntityHandler.categorized[ObjectCategory.PROJECTILES].clear()
    gun1: LaunchableGun = TestGun()
    gun2: LaunchableGun = TestGun()
    weapon: Weapon = Weapon(gun1, gun2)

    weapon.altfire((0.0, 0.0), 0.0, np.inf)

    assert len(EntityHandler.categorized[ObjectCategory.PROJECTILES]) != 0, "Weapon altfire does not work properly. No instance created."


@pytest.mark.randomize(min_num=0.25, max_num=10.0, ncalls=5)
def test_update(can_altfire: bool, shots_per_second1: float, shots_per_second2: float):
    updates_per_second: int = 60
    gun1: LaunchableGun = TestGun(shots_per_sec=shots_per_second1)
    gun2: Optional[LaunchableGun] = None
    if can_altfire: gun2: LaunchableGun = TestGun(shots_per_sec=shots_per_second2)
    weapon: Weapon = Weapon(gun1, gun2)
    delta: float = 1 / updates_per_second
    frame_count: int = 0

    weapon.fire((0.0, 0.0), 0.0, np.inf)
    weapon.altfire((0.0, 0.0), 0.0, np.inf)
    fire_worked: bool = False
    altfire_worked: bool = False
    while not fire_worked and not altfire_worked:
        fire_worked = weapon.fire((0.0, 0.0), 0.0, np.inf)
        altfire_worked = weapon.altfire((0.0, 0.0), 0.0, np.inf)
        frame_count += 1
        weapon.process(delta)

    if fire_worked: # frame_count-1 because we check inside the loop not at the start
        assert frame_count-1 == updates_per_second // shots_per_second1 + 1, "Weapon main gun cooldown is not properly updated."
    else: # altfire_worked
        assert frame_count-1 == updates_per_second // shots_per_second2 + 1, "Weapon alt gun cooldown is not properly updated."


if __name__ == '__main__':
    pass
