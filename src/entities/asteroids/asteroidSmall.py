
import arcade
from src.auxilary.ObjectCategory import ObjectCategory
from src.entities.asteroid import Asteroid


class AsteroidSmall(Asteroid):

    def __init__(self, starting_velocity: arcade.Vector, starting_position: arcade.Point) -> None:
        Asteroid.__init__(self, sprite_url="..\\resources\\sprites\\asteroid0.png",
                          belongs_to=ObjectCategory.MISC,
                          collides_with=[ObjectCategory.STATIC, ObjectCategory.ENEMIES, ObjectCategory.PLAYER, ObjectCategory.MISC],
                          hp_max=10.0, starting_velocity=starting_velocity, starting_position=starting_position)
