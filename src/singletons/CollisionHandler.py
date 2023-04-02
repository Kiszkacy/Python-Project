
import arcade
from src.singletons.Singleton import Singleton
from src.singletons.EntityHandler import EntityHandler
from src.interfaces.Collidable import Collidable

class CollisionHandler(metaclass=Singleton):

    # TODO doing detection collision here or in objects? 
    active_collidables: list[Collidable] = []

    @staticmethod
    def check_collision(element: Collidable and arcade.Sprite):
        layers = [EntityHandler.categorized[layer.value] for layer in element.collides_with]
        hits = arcade.check_for_collision_with_lists(element, layers)
        # TODO depending on how we set layers, filtering won't be necessary
        return [collided for collided in hits if isinstance(collided, Collidable)]


if __name__ == '__main__':
    pass
