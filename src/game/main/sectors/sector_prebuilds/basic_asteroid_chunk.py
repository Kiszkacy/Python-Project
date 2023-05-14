from arcade import SpriteList
import pickle

from src.game.main.entities.asteroids.big import AsteroidBig
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.sectors.chunk import Chunk
from src.game.main.entities.asteroids.medium import AsteroidMedium
from src.game.main.entities.asteroids.small import AsteroidSmall
from src.game.main.singletons.entity_handler import EntityHandler


class BasicAsteroidChunk(Chunk):
    objects: list[bytes] = [pickle.dumps(AsteroidSmall((0,0), (0,0))),
                            pickle.dumps(AsteroidMedium((0,0), (0,0))),
                            pickle.dumps(AsteroidBig((0,0), (0,0)))]

    def __init__(self, cumulative_prob, density: float = 0.005):
        super().__init__(density, [0.65, 0.3, 0.05], cumulative_prob)


    def generate(self, left_corner: tuple[int, int]):
        generated_sprites: SpriteList = super()._generate(left_corner)
        # TODO could add initial velocity for asteroids
        EntityHandler.extend(generated_sprites, ObjectCategory.MISC)
