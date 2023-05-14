from arcade import SpriteList

from src.game.main.entities.enemies.enemy_ship import EnemyShip
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.sectors.chunk import Chunk
from src.game.main.singletons.entity_handler import EntityHandler


class BasicEnemyChunk(Chunk):

    def __init__(self, cumulative_prob, density: float = 0.005):
        enemy_type1: EnemyShip = EnemyShip((0, 0))
        sprite_list: SpriteList = SpriteList()
        sprite_list.append(enemy_type1)
        super().__init__(density, sprite_list, [1.0], cumulative_prob)


    def generate(self, left_corner: tuple[int, int]):
        generated_sprites: SpriteList = super()._generate(left_corner)
        EntityHandler.extend(generated_sprites, ObjectCategory.ENEMIES)
