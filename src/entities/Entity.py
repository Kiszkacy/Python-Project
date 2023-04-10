
import arcade


class Entity(arcade.Sprite):

    def __init__(self, sprite_url: str) -> None:
        super().__init__(filename=sprite_url, hit_box_algorithm="None") # TODO check what happens here, there are 2 super classes !


if __name__ == '__main__':
    pass
