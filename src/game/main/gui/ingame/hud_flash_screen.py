from typing import Tuple

import arcade

from src.game.main.entities.player_ship import PlayerShip
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.interfaces.processable import Processable
from src.game.main.singletons.config import Config
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.util.math import map_range


class HUDFlashScreen(Processable):

    def __init__(self, player_ship: PlayerShip) -> None:
        self.shield_break: arcade.SpriteSolidColor = None
        self.damage_shield: arcade.SpriteSolidColor = None
        self.damage_hull: arcade.SpriteSolidColor = None
        self.flash_timer: float = 0.0
        self.active_flash: arcade.SpriteSolidColor = None

        self.player_ship: PlayerShip = player_ship
        self.previous_hp: float = player_ship.hp
        self.previous_shd: float = player_ship.shd

    def init(self) -> None:
        width: int = Config.Settings.get("SCREEN_WIDTH")
        height: int = Config.Settings.get("SCREEN_HEIGHT")
        self.shield_break = self.flash_screen_init(width, height, (87, 249, 195))
        self.damage_shield = self.flash_screen_init(width, height, (87, 217, 249))
        self.damage_hull = self.flash_screen_init(width, height, (245, 87, 87))

    def flash_screen_init(self, width: int, height: int, color: Tuple[int, int, int] | Tuple[int, int, int, int]) -> arcade.SpriteSolidColor:
        screen: arcade.SpriteSolidColor = arcade.SpriteSolidColor(width, height, color)
        screen.color = (0, 0, 0, 0)
        screen.position = (width // 2, height // 2)
        EntityHandler.add(screen, ObjectCategory.HUD)
        return screen

    def reset_screens(self) -> None:
        self.shield_break.color = (0, 0, 0, 0)
        self.damage_shield.color = (0, 0, 0, 0)
        self.damage_hull.color = (0, 0, 0, 0)

    def process(self, delta: float) -> None:
        if self.player_ship.shd < self.previous_shd and self.player_ship.shd > 0.0:
            self.reset_screens()  # reset old effects
            self.active_flash = self.damage_shield
            self.flash_timer = 0.8  # TODO constant
        elif self.player_ship.shd < self.previous_shd:  # shd <= 0.0
            self.reset_screens()  # reset old effects
            self.active_flash = self.shield_break
            self.flash_timer = 1.4  # TODO constant
        elif self.player_ship.hp < self.previous_hp:
            self.reset_screens()  # reset old effects
            self.active_flash = self.damage_hull
            self.flash_timer = 0.8  # TODO constant

        self.previous_shd = self.player_ship.shd
        self.previous_hp = self.player_ship.hp

        if self.flash_timer > 0.0:
            self.flash_timer -= delta
            if self.flash_timer <= 0.0: # last frame was the last one, clean up
                self.active_flash.color = (0, 0, 0, 0)
                self.active_flash = None
            else:
                self.active_flash.color = (255, 255, 255, int(map_range(self.flash_timer, 0.0, 2.0, 0, 255))) # TODO constant


if __name__ == '__main__':
    pass
