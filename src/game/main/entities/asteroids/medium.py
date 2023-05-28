
import arcade
import numpy as np

from src.game.main.entities.asteroids.asteroid import Asteroid
from src.game.main.entities.asteroids.small import AsteroidSmall
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.interfaces.destroyable import Destroyable
from src.game.main.interfaces.lootable import Lootable
from src.game.main.lootdrop.lootdrop import LootDrop
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.util.path_loader import get_absolute_resource_path
from src.game.main.util.rand import randrange, one_in
from src.game.main.lootdrop.loader import Loader as LootDropLoader


class AsteroidMedium(Asteroid, Lootable):
    LOOT_TABLE: LootDrop = LootDropLoader.load_from_json(get_absolute_resource_path("\\loottables\\asteroids\\medium.json"))

    def __init__(self, starting_velocity: arcade.Vector, starting_position: arcade.Point) -> None:
        sprite_path = get_absolute_resource_path("\\sprites\\asteroids\\medium.png")
        self.minable: bool = one_in(3)
        if self.minable: sprite_path = get_absolute_resource_path("\\sprites\\asteroids\\minable\\medium.png")
        Asteroid.__init__(self, sprite_url=sprite_path,
                          hp_max=50.0, mass=100.0, starting_velocity=starting_velocity,
                          starting_position=starting_position)
        if self.minable: self.color = (235,235,52)

    def destroy(self) -> Destroyable: # on death spawn small asteroids
        count: int = randrange(2, 4)
        for i in range(count):
            EntityHandler.add(
                AsteroidSmall(
                    starting_position=(self.position[0] + np.random.randint(-30, 30), self.position[1] + np.random.randint(-30, 30)),
                    starting_velocity=(np.random.randint(-10, 10), np.random.randint(-10, 10))
                ),
                ObjectCategory.NEUTRAL, True
            )
        if self.minable: self.drop(AsteroidMedium.LOOT_TABLE, self.position)
        super(AsteroidMedium, self).destroy()
        return self
