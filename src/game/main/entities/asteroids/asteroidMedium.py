
import arcade
import numpy as np

from src.game.main.entities.asteroids.asteroid import Asteroid
from src.game.main.entities.asteroids.asteroidSmall import AsteroidSmall
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.interfaces.destroyable import Destroyable
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.util.path_loader import get_absolute_resource_path


class AsteroidMedium(Asteroid):

    def __init__(self, starting_velocity: arcade.Vector, starting_position: arcade.Point) -> None:
        Asteroid.__init__(self, sprite_url=get_absolute_resource_path("\\sprites\\asteroid_med0.png"),
                          hp_max=50.0, mass=100.0, starting_velocity=starting_velocity,
                          starting_position=starting_position)

    def destroy(self) -> Destroyable: # on death spawn small asteroids
        count: int = np.random.randint(2, 4)
        for i in range(count):
            EntityHandler.add(
                AsteroidSmall(
                    starting_position=(self.position[0] + np.random.randint(-30, 30), self.position[1] + np.random.randint(-30, 30)),
                    starting_velocity=(np.random.randint(-10, 10), np.random.randint(-10, 10))
                ),
                ObjectCategory.MISC
            )
        super(AsteroidMedium, self).destroy()
        return self
