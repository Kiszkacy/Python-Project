from __future__ import annotations

import pytest

from src.game.main.entities.player_ship import PlayerShip # TODO this crashes tests if removed ??? (cycled imports?)

from src.game.main.entities.structure import Structure
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.util.path_loader import get_absolute_resource_path


@pytest.mark.randomize(ncalls=1)
def test_power_regen_request():
    structure: Structure = Structure(sprite_url=get_absolute_resource_path("\\sprites\\error.png"), # this shouldnt be here
                                     mass=10,
                                     belongs_to=ObjectCategory.NEUTRAL,
                                     collides_with=[],
                                     power_max=10.0)

    structure.set_power(structure.power - 1.0)

    assert structure.power_timer_online == True


# TODO finish


if __name__ == '__main__':
    pass
