
import arcade

from src.game.main.enums.object_category import ObjectCategory
from src.game.main.singletons.singleton import Singleton


class EntityHandler(metaclass=Singleton):

    # TODO decide which category should use spatial hashes
    categorized: list[arcade.SpriteList] = [arcade.SpriteList(use_spatial_hash=True) for _ in ObjectCategory]

    @staticmethod
    def add(sprite: arcade.Sprite, category: ObjectCategory) -> None:
        EntityHandler.categorized[category.value].append(sprite)

    @staticmethod
    def draw_all() -> None:
        for layer in EntityHandler.categorized:
            layer.draw()

    @staticmethod
    def draw(category: ObjectCategory) -> None:
        EntityHandler.categorized[category].draw()

    @staticmethod
    def on_update(delta_time: float, category: ObjectCategory) -> None:
        EntityHandler.categorized[category.value].on_update(delta_time)

    @staticmethod
    def initialize() -> None:
        for category in EntityHandler.categorized:
            category.initialize()


if __name__ == '__main__':
    pass
