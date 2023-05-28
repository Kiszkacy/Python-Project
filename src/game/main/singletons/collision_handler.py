from typing import List

import arcade
import numpy as np

from src.game.main.interfaces.bucketable import Bucketable
from src.game.main.interfaces.collidable import Collidable
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.singletons.singleton import Singleton
from src.game.main.util.math import intersects_lines


class CollisionHandler(metaclass=Singleton):

    @staticmethod
    def check_collision(element: Collidable and arcade.Sprite, bucketable: bool = False) -> list[Collidable]:
        if bucketable:
            object: Bucketable = element # we are sure that object is Bucketable if boolean is set to true ! might create problems if careless
            layers: List[arcade.SpriteList] = [EntityHandler.buckets[object.bucket_y_idx][object.bucket_x_idx][layer.value] for layer in element.collides_with]
            hits: List[arcade.Sprite] = arcade.check_for_collision_with_lists(element, layers)
            return [collided for collided in hits]
        else:
            layers: List[arcade.SpriteList] = [EntityHandler.categorized[layer.value] for layer in element.collides_with]
            hits: List[arcade.Sprite] = arcade.check_for_collision_with_lists(element, layers)
            # TODO i removed filtering check if still works | also IDE shows warnings now
            return [collided for collided in hits] # if isinstance(collided, Collidable)

    @staticmethod
    def get_collision_vector(main_obj: arcade.Sprite, collided_with: arcade.Sprite) -> np.ndarray | None:
        hit_box1 = main_obj.get_adjusted_hit_box()
        hit_box2 = collided_with.get_adjusted_hit_box()
        len1, len2 = len(hit_box1), len(hit_box2)
        intersection_points = []

        # finding intersection points between each pair of segments belonging two hitbox1 and hitbox2
        for i in range(len(hit_box1)):
            i1, i2 = i, (i + 1) % len1
            for j in range(len(hit_box2)):
                j1, j2 = j, (j + 1) % len2
                # finding intersection point between two segments belonging two hitbox1 and hitbox2
                intersection_point = intersects_lines((hit_box1[i1], hit_box1[i2]), (hit_box2[j1], hit_box2[j2]))
                if intersection_point is not None:
                    intersection_points.append(intersection_point)

        total_intersections = len(intersection_points)
        # method should be called only when we know that collision occurred
        # None can mean that there is no collision or one hitbox contains the other
        if total_intersections == 0:
            return None
        # calculating "centre" of collision
        centre = sum(intersection_points) / total_intersections
        # vector pointing from the center of collision tho the center of main_obj
        vector = np.array((main_obj.center_x - centre[0], main_obj.center_y - centre[1]))
        return vector


if __name__ == '__main__':
    pass
