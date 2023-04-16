
import arcade
from src.singletons.Singleton import Singleton
from src.auxilary.ObjectCategory import ObjectCategory


class EntityHandler(metaclass=Singleton):

    # TODO decide which category should use spatial hashes
    categorized: list[arcade.SpriteList] = [arcade.SpriteList(use_spatial_hash=True) for _ in ObjectCategory]
    barrier_list: arcade.AStarBarrierList = None

    @staticmethod
    def add(sprite: arcade.Sprite, category: ObjectCategory) -> None:
        EntityHandler.categorized[category].append(sprite)

    @staticmethod
    def draw() -> None:
        for layer in EntityHandler.categorized:
            layer.draw()

    @staticmethod
    def on_update(delta_time: float, category: ObjectCategory) -> None:
        EntityHandler.categorized[category].on_update(delta_time)

    @staticmethod
    def initialize() -> None:
        for category in EntityHandler.categorized:
            category.initialize()


    @staticmethod
    def update_barrier_list():
        from src.entities.EnemyShip import EnemyShip
        EntityHandler.barrier_list = arcade.AStarBarrierList(EnemyShip((0, 0)),
                                                             # TODO this values shouldn't be hardcoded
                                                             EntityHandler.categorized[ObjectCategory.STATIC],
                                                             128,
                                                             -2000, 2000, -2000, 2000)


if __name__ == '__main__':
    pass
