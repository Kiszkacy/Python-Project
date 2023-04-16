import os

import pytest

from src.game.main.entities.entity import Entity
from src.game.main.util.path_loader import get_absolute_resource_path


@pytest.mark.slow
@pytest.mark.randomize(ncalls=1)
def test_sprite_load():
    root: str = get_absolute_resource_path("\\sprites\\")

    for path, subdirs, files in os.walk(root):
        for name in files:
            if name.lower().endswith((".png", ".jpg", ".jpeg")):
                try:
                    entity: Entity = Entity(os.path.join(path, name))
                except Exception:
                    raise Exception(f"Could not load {os.path.join(path, name)} sprite.")


if __name__ == '__main__':
    pass




