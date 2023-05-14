
import arcade

from src.game.main.entities.asteroids.asteroid import Asteroid
from src.game.main.util.path_loader import get_absolute_resource_path


class AsteroidSmall(Asteroid):

    def __init__(self, starting_velocity: arcade.Vector, starting_position: arcade.Point) -> None:
        Asteroid.__init__(self, sprite_url=get_absolute_resource_path("\\sprites\\asteroids\\small.png"),
                          hp_max=15.0, mass=30.0, starting_velocity=starting_velocity,
                          starting_position=starting_position)
