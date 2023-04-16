
import arcade

from src.game.main.entities.entity import Entity
from src.game.main.interfaces.processable import Processable
from src.game.main.util.path_loader import get_absolute_resource_path


class BackgroundDrawer(Processable):

    def __init__(self) -> None:
        self.background: arcade.SpriteList = arcade.SpriteList()
        self.midground: arcade.SpriteList = arcade.SpriteList()
        self.foreground: arcade.SpriteList = arcade.SpriteList()
        self.tracked_entity: Entity = None
        self.sprite_size: arcade.Vector = (2560, 1440)

    def init(self, tracked_entity: Entity) -> None:
        self.tracked_entity = tracked_entity

        for i in range(4):
            self.background.append(arcade.Sprite(get_absolute_resource_path("\\sprites\\bg0.png")))
            self.midground.append(arcade.Sprite(get_absolute_resource_path("\\sprites\\bg1.png")))
            self.foreground.append(arcade.Sprite(get_absolute_resource_path("\\sprites\\bg2-correct.png")))

    def process(self, delta: float) -> None:
        # move sprites according to tracked_entity position
        target_pos: arcade.Vector = self.tracked_entity.position
        target_x_cell: int = target_pos[0] // self.sprite_size[0]
        target_y_cell: int = target_pos[1] // self.sprite_size[1]
        # main sprites
        position: arcade.Vector = (0 + target_x_cell*self.sprite_size[0] + self.sprite_size[0]//2,
                                   0 + target_y_cell*self.sprite_size[1] + self.sprite_size[1]//2)
        self.background[0].position = position
        self.midground[0].position = position
        self.foreground[0].position = position
        # now get corresponding cell corner in which tracked_entity is inside
        subcell_pos: arcade.Vector = (target_pos[0] - target_x_cell*self.sprite_size[0],
                                      target_pos[1] - target_y_cell*self.sprite_size[1])
        left_half: bool = True if subcell_pos[0] <= self.sprite_size[0] // 2 else False
        top_half: bool = True if subcell_pos[1] <= self.sprite_size[1] // 2 else False
        vertical_offset: int = -1 if left_half else 1
        horizontal_offset: int = -1 if top_half else 1
        # side sprites
        position = (0 + (target_x_cell+vertical_offset)*self.sprite_size[0] + self.sprite_size[0]//2,
                    0 + target_y_cell*self.sprite_size[1] + self.sprite_size[1]//2)
        self.background[1].position = position
        self.midground[1].position = position
        self.foreground[1].position = position
        # top/bottom sprites
        position = (0 + target_x_cell*self.sprite_size[0] + self.sprite_size[0]//2,
                    0 + (target_y_cell+horizontal_offset)*self.sprite_size[1] + self.sprite_size[1]//2)
        self.background[2].position = position
        self.midground[2].position = position
        self.foreground[2].position = position
        # diagonal sprites
        position = (0 + (target_x_cell+vertical_offset)*self.sprite_size[0] + self.sprite_size[0]//2,
                    0 + (target_y_cell+horizontal_offset)*self.sprite_size[1] + self.sprite_size[1]//2)
        self.background[3].position = position
        self.midground[3].position = position
        self.foreground[3].position = position

    def draw(self) -> None: # optimize this
        self.background.draw()
        self.midground.draw()
        self.foreground.draw()


if __name__ == '__main__':
    pass
