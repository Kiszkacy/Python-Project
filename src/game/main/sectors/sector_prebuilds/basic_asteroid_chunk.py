from arcade import SpriteList

from src.game.main.sectors.chunk import Chunk
from src.game.main.entities.asteroids.asteroidMedium import AsteroidMedium
from src.game.main.entities.asteroids.asteroidSmall import AsteroidSmall


class BasicAsteroidChunk(Chunk):

    def __init__(self, cumulative_prob, density: float = 0.005):

        sprite_list: SpriteList = SpriteList()
        sprite_list.append(AsteroidMedium((0,0), (0,0)))
        sprite_list.append(AsteroidSmall((0,0), (0,0)))
        super().__init__(density, sprite_list, [0.3, 0.7], cumulative_prob)