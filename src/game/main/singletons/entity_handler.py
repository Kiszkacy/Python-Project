from __future__ import annotations
from typing import List, Optional

import arcade

import src.game.main.entities.player_ship as p
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.interfaces.bucketable import Bucketable
from src.game.main.singletons.config import Config
from src.game.main.singletons.singleton import Singleton


class EntityHandler(metaclass=Singleton):

    # TODO decide which category should use spatial hashes
    categorized: List[arcade.SpriteList] = [arcade.SpriteList() for _ in ObjectCategory]
    barrier_list: arcade.AStarBarrierList = None
    player: Optional[p.PlayerShip] = None
    buckets: List[List[List[arcade.SpriteList]]] = []
    bucket_y_count: int = 0
    bucket_x_count: int = 0

    @staticmethod
    def extend(sprites: arcade.SpriteList, category: ObjectCategory, bucketable: bool = False) -> None:
        EntityHandler.categorized[category].extend(sprites)
        if bucketable:
            bs: float = Config.Constants.get("BUCKET_SIZE")
            for sprite in sprites:
                object: Bucketable = sprite # we are sure that object is Bucketable if boolean is set to true ! might create problems if careless
                bucket_x: int = int(object.position[0] // bs)
                bucket_y: int = int(object.position[1] // bs)
                EntityHandler.buckets[bucket_y][bucket_x][category].append(sprite)
                object.bucket_y_idx = bucket_y
                object.bucket_x_idx = bucket_x

    @staticmethod
    def add(sprite: arcade.Sprite, category: ObjectCategory, bucketable: bool = False) -> None:
        EntityHandler.categorized[category].append(sprite)
        if bucketable:
            object: Bucketable = sprite # we are sure that object is Bucketable if boolean is set to true ! might create problems if careless
            bs: float = Config.Constants.get("BUCKET_SIZE")
            bucket_x: int = int(object.position[0] // bs)
            bucket_y: int = int(object.position[1] // bs)
            EntityHandler.buckets[bucket_y][bucket_x][category].append(sprite)
            object.bucket_y_idx = bucket_y
            object.bucket_x_idx = bucket_x

    @staticmethod
    def bucket_init(sector_width: int, sector_height: int) -> None:
        bs: float = Config.Constants.get("BUCKET_SIZE")
        bbs: float = Config.Constants.get("BUCKET_BUFFER_SIZE")
        cs: float = Config.Constants.get("CHUNK_SIZE")

        total_width: float = sector_width * cs + bbs * 2
        # print(total_width, int(total_width//bs) + 1)
        EntityHandler.bucket_x_count = int(total_width//bs) + 1
        total_height: float = sector_height * cs + bbs * 2
        EntityHandler.bucket_y_count = int(total_height//bs) + 1
        # print(total_height, int(total_height // bs) + 1)
        print(sector_width, sector_height)

        EntityHandler.buckets = [[[arcade.SpriteList(use_spatial_hash=True)
                                   for _ in ObjectCategory]
                                  for _ in range(EntityHandler.bucket_x_count)]
                                 for _ in range(EntityHandler.bucket_y_count)]

        # init lists
        for y in range(EntityHandler.bucket_y_count):
            for x in range(EntityHandler.bucket_x_count):
                for i in ObjectCategory:
                    EntityHandler.buckets[y][x][i].initialize()

    @staticmethod
    def draw_all() -> None:
        for layer in EntityHandler.categorized:
            layer.draw()

    @staticmethod
    def draw(category: ObjectCategory) -> None:
        EntityHandler.categorized[category].draw()

    # @staticmethod
    # def draw_close_buckets(category: ObjectCategory) -> None:
    #     pos: arcade.Point = EntityHandler.player.position
    #     bs: float = Config.Constants.get("BUCKET_SIZE")
    #     player_bucket_x: int = int(pos[0] // bs)
    #     player_bucket_y: int = int(pos[1] // bs)
    #     for y in range(-1, 1+1):
    #         # if out of range skip
    #         if player_bucket_y + y < 0 or player_bucket_y + y > EntityHandler.bucket_y_count: continue
    #         for x in range(-1, 1+1):
    #             # if out of range skip
    #             if player_bucket_x + x < 0 or player_bucket_x + x > EntityHandler.bucket_x_count: continue
    #             # update bucket
    #             EntityHandler.buckets[player_bucket_y + y][player_bucket_x + x][category].draw()
    #             if category == ObjectCategory.ENEMIES:
    #                 print("DRAW", player_bucket_x + x, player_bucket_y + y)

    @staticmethod
    def update(delta_time: float, category: ObjectCategory) -> None:
        EntityHandler.categorized[category].on_update(delta_time)

    @staticmethod
    def update_close_buckets(delta: float, category: ObjectCategory) -> None:
        # if category == ObjectCategory.ENEMIES: return
        pos: arcade.Point = EntityHandler.player.position
        bs: float = Config.Constants.get("BUCKET_SIZE")
        player_bucket_x: int = int(pos[0] // bs)
        player_bucket_y: int = int(pos[1] // bs)
        for y in range(-1, 1+1):
            # if out of range skip
            if player_bucket_y + y < 0 or player_bucket_y + y > EntityHandler.bucket_y_count: continue
            for x in range(-1, 1+1):
                # if out of range skip
                if player_bucket_x + x < 0 or player_bucket_x + x > EntityHandler.bucket_x_count: continue
                # update bucket
                EntityHandler.buckets[player_bucket_y + y][player_bucket_x + x][category].on_update(delta)

    @staticmethod
    def initialize() -> None:
        for category in EntityHandler.categorized:
            category.initialize()

    @staticmethod
    def update_barrier_list(sector_width: float, sector_height: float) -> None:
        from src.game.main.entities.enemies.enemy import Enemy
        cs: float = Config.Constants.get("CHUNK_SIZE")
        EntityHandler.barrier_list = arcade.AStarBarrierList(Enemy((0, 0)),
                                                             EntityHandler.categorized[ObjectCategory.STATIC],
                                                             grid_size=128,
                                                             left=-Config.Constants.get("BUCKET_BUFFER_SIZE"),
                                                             right=sector_width*cs + Config.Constants.get("BUCKET_BUFFER_SIZE"),
                                                             bottom=-Config.Constants.get("BUCKET_BUFFER_SIZE"),
                                                             top=sector_height*cs + Config.Constants.get("BUCKET_BUFFER_SIZE"))


if __name__ == '__main__':
    pass
