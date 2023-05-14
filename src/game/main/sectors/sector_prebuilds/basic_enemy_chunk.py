from arcade import SpriteList
import pickle

from src.game.main.entities.enemies.enemy_ship import EnemyShip
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.sectors.chunk import Chunk
from src.game.main.singletons.entity_handler import EntityHandler


class BasicEnemyChunk(Chunk):
    objects: list[bytes] = [pickle.dumps(EnemyShip((0, 0)))]

    def __init__(self, cumulative_prob, density: float = 0.005):
        super().__init__(density, [1.0], cumulative_prob)


    def generate(self, left_corner: tuple[int, int]):
        generated_sprites: SpriteList = super()._generate(left_corner)
        for elem in generated_sprites:
            elem: EnemyShip = elem
            elem.initialize()
        EntityHandler.extend(generated_sprites, ObjectCategory.ENEMIES)
