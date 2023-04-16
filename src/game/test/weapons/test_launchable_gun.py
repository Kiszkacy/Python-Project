
import numpy as np
import pytest

from src.game.main.enums.object_category import ObjectCategory
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.weapons.launchable_gun import LaunchableGun


@pytest.mark.randomize(min_num=0.25, max_num=10.0, ncalls=100)
def test_shot_cooldown(shots_per_second: float):
    updates_per_second: int = 60
    gun: LaunchableGun = LaunchableGun(shots_per_sec=shots_per_second)
    delta: float = 1 / updates_per_second
    frame_count: int = 0

    gun.shoot((0.0, 0.0), 0.0)
    while not gun.can_shoot(np.inf):
        frame_count += 1
        gun.process(delta)

    assert frame_count == updates_per_second // shots_per_second + 1, "Shot cooldown frame count does not match expected amount."

@pytest.mark.slow
@pytest.mark.randomize(min_num=1, max_num=36, ncalls=100)
def test_barrel_count(barrel_count: int):
    EntityHandler.categorized[ObjectCategory.PROJECTILES].clear()
    gun: LaunchableGun = LaunchableGun(barrel_count=barrel_count)
    gun.shoot((0.0, 0.0), 0.0)

    assert len(EntityHandler.categorized[ObjectCategory.PROJECTILES]) == barrel_count, "Created amount of instances does not match barrel count."


if __name__ == '__main__':
    pass




