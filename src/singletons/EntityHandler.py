
import arcade
from src.singletons.Singleton import Singleton
from src.auxilary.ObjectCategory import ObjectCategory


class EntityHandler(metaclass=Singleton):

    # TODO decide which category should use spatial hashes
    categorized: list[arcade.SpriteList] = [arcade.SpriteList() for _ in ObjectCategory]

    @staticmethod
    def add(sprite: arcade.Sprite, category: ObjectCategory) -> None:
        EntityHandler.categorized[category.value].append(sprite)

    @staticmethod
    def draw() -> None:
        for layer in EntityHandler.categorized:
            layer.draw()

    @staticmethod
    def on_update(delta_time: float, category: ObjectCategory) -> None:
        EntityHandler.categorized[category.value].on_update(delta_time)

    @staticmethod
    def initialize() -> None:
        for category in EntityHandler.categorized:
            category.initialize()


if __name__ == '__main__':
    pass
