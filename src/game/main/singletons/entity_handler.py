
import arcade

from src.game.main.enums.object_category import ObjectCategory
from src.game.main.singletons.config import Config
from src.game.main.singletons.singleton import Singleton


class EntityHandler(metaclass=Singleton):

    # TODO decide which category should use spatial hashes
    categorized: list[arcade.SpriteList] = [arcade.SpriteList(use_spatial_hash=True) for _ in ObjectCategory]
    barrier_list: arcade.AStarBarrierList = None

    @staticmethod
    def extend(sprite: arcade.SpriteList, category: ObjectCategory) -> None:
        EntityHandler.categorized[category].extend(sprite)

    @staticmethod
    def add(sprite: arcade.Sprite, category: ObjectCategory) -> None:
        EntityHandler.categorized[category].append(sprite)

    @staticmethod
    def draw_all() -> None:
        for layer in EntityHandler.categorized:
            layer.draw()

    @staticmethod
    def draw(category: ObjectCategory) -> None:
        EntityHandler.categorized[category].draw()

    @staticmethod
    def on_update(delta_time: float, category: ObjectCategory) -> None:
        EntityHandler.categorized[category].on_update(delta_time)

    @staticmethod
    def initialize() -> None:
        for category in EntityHandler.categorized:
            category.initialize()

    @staticmethod
    def update_barrier_list():
        from src.game.main.entities.enemies.enemy_ship import EnemyShip
        EntityHandler.barrier_list = arcade.AStarBarrierList(EnemyShip((0, 0)),
                                                             # TODO this values shouldn't be hardcoded, very TMP
                                                             EntityHandler.categorized[ObjectCategory.STATIC],
                                                             128,
                                                             -2000, Config.Constants["CHUNK_SIZE"]*10, -2000, Config.Constants["CHUNK_SIZE"]*10)


if __name__ == '__main__':
    pass
