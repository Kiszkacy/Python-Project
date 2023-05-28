
import arcade

from src.game.main.util.force_slots import Slots
from src.game.main.util.path_loader import get_absolute_resource_path




class Entity(arcade.Sprite):
    """Basic sprite class."""
    def __init__(self, sprite_url: str = get_absolute_resource_path("\\sprites\\error.png")) -> None:
        super().__init__(filename=sprite_url, hit_box_algorithm="None") # TODO check what happens here, there are 2 super classes !


if __name__ == '__main__':
    pass

