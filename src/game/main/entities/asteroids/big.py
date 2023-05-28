
import arcade
import numpy as np

from src.game.main.entities.asteroids.asteroid import Asteroid
from src.game.main.entities.asteroids.small import AsteroidSmall
from src.game.main.entities.asteroids.medium import AsteroidMedium
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.interfaces.destroyable import Destroyable
from src.game.main.interfaces.lootable import Lootable
from src.game.main.lootdrop.lootdrop import LootDrop
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.util.path_loader import get_absolute_resource_path
from src.game.main.util.rand import randrange, one_in
from src.game.main.lootdrop.loader import Loader as LootDropLoader


class AsteroidBig(Asteroid, Lootable):

    LOOT_TABLE: LootDrop = LootDropLoader.load_from_json(get_absolute_resource_path("\\loottables\\asteroids\\big.json"))

    def __init__(self, starting_velocity: arcade.Vector, starting_position: arcade.Point) -> None:
        sprite_path = get_absolute_resource_path("\\sprites\\asteroids\\big.png")
        self.minable: bool = one_in(3)
        if self.minable: sprite_path = get_absolute_resource_path("\\sprites\\asteroids\\minable\\big.png")
        Asteroid.__init__(self, sprite_url=sprite_path,
                          hp_max=100.0, mass=100.0, starting_velocity=starting_velocity, # TODO increase mass in the future
                          starting_position=starting_position)
        if self.minable: self.color = (235,235,52)

    def destroy(self) -> Destroyable: # on death spawn medium and small asteroids
        for i in range(randrange(1, 2)):
            EntityHandler.add(
                AsteroidMedium(
                    starting_position=(self.position[0] + np.random.randint(-120, 120), self.position[1] + np.random.randint(-120, 120)),
                    starting_velocity=(np.random.randint(-5, 5), np.random.randint(-5, 5))
                ),
                ObjectCategory.NEUTRAL, True
            )

        for i in range(randrange(1, 3)):
            EntityHandler.add(
                AsteroidSmall(
                    starting_position=(self.position[0] + np.random.randint(-120, 120), self.position[1] + np.random.randint(-120, 120)),
                    starting_velocity=(np.random.randint(-5, 5), np.random.randint(-5, 5))
                ),
                ObjectCategory.NEUTRAL, True
            )
        if self.minable: self.drop(AsteroidBig.LOOT_TABLE, self.position)
        super(AsteroidBig, self).destroy()
        return self
