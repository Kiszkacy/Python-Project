
from arcade import SpriteList
import pickle

from src.game.main.entities.enemies.enemy import Enemy
from src.game.main.entities.enemies.enemy_basic import EnemyBasic
from src.game.main.entities.enemies.enemy_special import EnemySpecial
from src.game.main.entities.enemies.enemy_tanky import EnemyTanky
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.sectors.chunk import Chunk
from src.game.main.singletons.entity_handler import EntityHandler


class EnemyFleetChunk(Chunk):
    objects: list[bytes] = [pickle.dumps(EnemySpecial((0, 0))),
                            pickle.dumps(EnemyTanky((0, 0)))]

    def __init__(self, cumulative_prob, density: float = 0.015):
        super().__init__(density, [0.5, 0.5], cumulative_prob)

    def generate(self, left_corner: tuple[int, int]):
        generated_sprites: SpriteList = super()._generate(left_corner)
        for elem in generated_sprites:
            elem: Enemy = elem
            elem.initialize()
        EntityHandler.extend(generated_sprites, ObjectCategory.ENEMIES)
