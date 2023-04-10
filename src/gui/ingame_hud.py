
from typing import Tuple
import arcade
from src.auxilary.ObjectCategory import ObjectCategory
from src.entities.PlayerShip import PlayerShip
from src.interfaces.Processable import Processable
from src.singletons.Config import Config
from src.singletons.EntityHandler import EntityHandler


class IngameHUD(Processable):

    def __init__(self, player_ship: PlayerShip) -> None:
        self.player_ship: PlayerShip = player_ship
        self.weapon_icons: list[arcade.SpriteSolidColor] = []
        self.health_bar: list[arcade.SpriteSolidColor] = []
        self.shield_bar: list[arcade.SpriteSolidColor] = []
        self.power_bar: list[arcade.SpriteSolidColor] = []
        self.mission_objective: arcade.SpriteSolidColor = None


    def init(self) -> None:
        # weapon icons
        for i in range(Config.Constants.get("WEAPONS_MAX")): # TODO make active only if player has that many weapons
            self.weapon_icons.append(arcade.SpriteSolidColor(64, 64, (192, 192, 192, 128))) # TODO add ui scaling ?
            self.weapon_icons[i].position = (48 + 80*i, Config.Settings.get("SCREEN_HEIGHT")-48)
            EntityHandler.add(self.weapon_icons[i], ObjectCategory.HUD)
        # health, shield and power bar
        self.health_bar.append(arcade.SpriteSolidColor(320, 32, (192, 192, 192, 192)))
        self.health_bar.append(arcade.SpriteSolidColor(320-8, 32-8, (48, 48, 48, 192)))
        self.health_bar.append(arcade.SpriteSolidColor(320-8, 32-8, (255, 78, 108, 192)))
        health_bar_pos: Tuple[int, int] = (192, 48+48)

        self.shield_bar.append(arcade.SpriteSolidColor(320, 32, (192, 192, 192, 192)))
        self.shield_bar.append(arcade.SpriteSolidColor(320-8, 32-8, (48, 48, 48, 192)))
        self.shield_bar.append(arcade.SpriteSolidColor(320-8, 32-8, (78, 203, 255, 192)))
        shield_bar_pos: Tuple[int, int] = (192, 48)

        self.power_bar.append(arcade.SpriteSolidColor(320, 32, (192, 192, 192, 192)))
        self.power_bar.append(arcade.SpriteSolidColor(320-8, 32-8, (48, 48, 48, 192)))
        self.power_bar.append(arcade.SpriteSolidColor(320-8, 32-8, (161, 78, 255, 192)))
        power_bar_pos: Tuple[int, int] = (Config.Settings.get("SCREEN_WIDTH")//2, Config.Settings.get("SCREEN_HEIGHT")-48)

        for i in range(3):
            EntityHandler.add(self.health_bar[i], ObjectCategory.HUD)
            self.health_bar[i].position = health_bar_pos
            EntityHandler.add(self.shield_bar[i], ObjectCategory.HUD)
            self.shield_bar[i].position = shield_bar_pos
            EntityHandler.add(self.power_bar[i], ObjectCategory.HUD)
            self.power_bar[i].position = power_bar_pos
        # mission windows
        self.mission_objective = arcade.SpriteSolidColor(320, 160, (192, 192, 192, 128))
        self.mission_objective.position = (Config.Settings.get("SCREEN_WIDTH")-16 - 320//2, Config.Settings.get("SCREEN_HEIGHT")-16 - 160//2)
        EntityHandler.add(self.mission_objective, ObjectCategory.HUD)


    def process(self, delta: float) -> None:
        # update active weapon
        weapon_idx: int = self.player_ship.weapon_idx
        for i in range(Config.Constants.get("WEAPONS_MAX")):
            self.weapon_icons[i].color = (128, 128, 128)
        self.weapon_icons[weapon_idx].color = (255, 255, 255)
        # update player bars
        active_idx: int = 2
        left_anchor: float = self.health_bar[active_idx].left
        self.health_bar[active_idx].width = max((self.player_ship.hp / self.player_ship.hp_max) * (320-8), 1) # TODO tmp max fix
        self.health_bar[active_idx].left = left_anchor
        left_anchor = self.shield_bar[active_idx].left
        self.shield_bar[active_idx].width = max((self.player_ship.shd / self.player_ship.shd_max) * (320-8), 1) # TODO tmp max fix
        self.shield_bar[active_idx].left = left_anchor
        left_anchor = self.power_bar[active_idx].left
        self.power_bar[active_idx].width = max((self.player_ship.power / self.player_ship.power_max) * (320-8), 1) # TODO tmp max fix
        self.power_bar[active_idx].left = left_anchor


if __name__ == '__main__':
    pass
