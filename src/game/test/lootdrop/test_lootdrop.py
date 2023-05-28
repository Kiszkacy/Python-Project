from typing import List, Tuple

import numpy as np
import pytest

from src.game.main.lootdrop.loader import Loader
from src.game.main.lootdrop.lootdrop import LootDrop
from src.game.main.util.path_loader import get_absolute_resource_path


@pytest.mark.randomize(ncalls=1)
def test_created_item_count():
    files: List[str] = ["table01.json", "table02.json", "table03.json", "table04.json", "table05.json"]
    count_range: List[Tuple[int, int]] = [(1,2), (1,4), (4,5), (3,15), (1,5)]

    for file, crange in zip(files, count_range):
        ld: LootDrop = Loader.load_from_json(get_absolute_resource_path(f"\\test\\loottables\\{file}"))
        for _ in range(1_000):
            assert crange[0] <= len(ld.calc()) <= crange[1], "Lootdrop created item count does not match expected amount."


if __name__ == '__main__':
    pass
