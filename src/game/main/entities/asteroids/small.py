
import arcade

from src.game.main.entities.asteroids.asteroid import Asteroid
from src.game.main.interfaces.destroyable import Destroyable
from src.game.main.interfaces.lootable import Lootable
from src.game.main.lootdrop.lootdrop import LootDrop
from src.game.main.util.path_loader import get_absolute_resource_path
from src.game.main.util.rand import one_in
from src.game.main.lootdrop.loader import Loader as LootDropLoader


class AsteroidSmall(Asteroid, Lootable):

    LOOT_TABLE: LootDrop = LootDropLoader.load_from_json(get_absolute_resource_path("\\loottables\\asteroids\\small.json"))

    def __init__(self, starting_velocity: arcade.Vector, starting_position: arcade.Point) -> None:
        sprite_path = get_absolute_resource_path("\\sprites\\asteroids\\small.png")
        self.minable: bool = one_in(3)
        if self.minable: sprite_path = get_absolute_resource_path("\\sprites\\asteroids\\minable\\small.png")
        Asteroid.__init__(self, sprite_url=sprite_path,
                          hp_max=15.0, mass=30.0, starting_velocity=starting_velocity,
                          starting_position=starting_position)
        if self.minable: self.color = (235,235,52)

    def destroy(self) -> Destroyable:
        if self.minable: self.drop(AsteroidSmall.LOOT_TABLE, self.position)
        return super(AsteroidSmall, self).destroy()
