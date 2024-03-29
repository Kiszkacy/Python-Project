
from typing import Tuple
import arcade

from src.game.main.entities.player_ship import PlayerShip
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.gui.ingame.hud_flash_screen import HUDFlashScreen
from src.game.main.gui.ingame.hud_out_of_bounds_warning import HUDOutOfBounds
from src.game.main.gui.ingame.hud_waypoint import HUDWaypoint
from src.game.main.interfaces.processable import Processable
from src.game.main.quests.quest_tracker import QuestTracker
from src.game.main.quests.quest_type import QuestType
from src.game.main.singletons.config import Config
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.util.math import clamp


class HUD(Processable):

    def __init__(self, main_quest: QuestTracker, side_quest: QuestTracker) -> None:
        self.player_ship: PlayerShip = EntityHandler.player

        self.weapon_icons: list[arcade.SpriteSolidColor] = []
        self.health_bar: list[arcade.SpriteSolidColor] = []
        self.shield_bar: list[arcade.SpriteSolidColor] = []
        self.power_bar: list[arcade.SpriteSolidColor] = []
        self.inventory_bar: list[arcade.SpriteSolidColor] = []
        self.dash_bars: list[arcade.SpriteSolidColor] = []
        self.mission_objective: arcade.SpriteSolidColor = None
        self.main_quest_tracker: QuestTracker = main_quest
        self.main_quest_text: arcade.Text = None
        self.side_quest_tracker: QuestTracker = side_quest
        self.side_quest_text: arcade.Text = None
        self.hud_flash_screen: HUDFlashScreen = HUDFlashScreen()
        self.hud_waypoint: HUDWaypoint = HUDWaypoint()
        self.hud_out_of_bounds: HUDOutOfBounds = HUDOutOfBounds()


    def init(self) -> None:
        # weapon icons
        for i in range(Config.Constants.get("WEAPONS_MAX")): # TODO make active only if player has that many weapons
            self.weapon_icons.append(arcade.SpriteSolidColor(64, 64, (192, 192, 192, 128))) # TODO add ui scaling ?
            self.weapon_icons[i].position = (48 + 80*i, Config.Settings.get("SCREEN_HEIGHT")-48)
            EntityHandler.add(self.weapon_icons[i], ObjectCategory.HUD)
        # health, shield and power bar
        self.bar_init(320, 32, 8, (255, 78, 108, 192), (48, 48, 48, 192), (192, 192, 192, 192), (192, 48+48), self.health_bar)
        self.bar_init(320, 32, 8, (78, 203, 255, 192), (48, 48, 48, 192), (192, 192, 192, 192), (192, 48), self.shield_bar)
        self.bar_init(320, 32, 8, (161, 78, 255, 192), (48, 48, 48, 192), (192, 192, 192, 192),
                      (Config.Settings.get("SCREEN_WIDTH")//2, Config.Settings.get("SCREEN_HEIGHT")-48), self.power_bar)
        # inventory bar
        self.bar_init(160, 32, 8, (217, 137, 52, 192), (48, 48, 48, 192), (192, 192, 192, 192),
                      (Config.Settings.get("SCREEN_WIDTH") - 112, 48), self.inventory_bar)
        # dash bars
        self.dash_bars_init()
        # mission windows
        self.mission_objective = arcade.SpriteSolidColor(320, 120, (192, 192, 192, 128))
        self.mission_objective.position = (Config.Settings.get("SCREEN_WIDTH")-16 - 320//2, Config.Settings.get("SCREEN_HEIGHT")-16 - 120//2)
        EntityHandler.add(self.mission_objective, ObjectCategory.HUD)
        # quest texts
        self.main_quest_text = arcade.Text(self.main_quest_tracker.quest.get_progress_status_text(),
                                           Config.Settings.get("SCREEN_WIDTH")-16 - 320//2,
                                           Config.Settings.get("SCREEN_HEIGHT")+8 - 120//2,
                                           color=(255,255,255), anchor_x="center", font_size=16)
        self.side_quest_text = arcade.Text(self.side_quest_tracker.quest.get_progress_status_text(),
                                           Config.Settings.get("SCREEN_WIDTH")-16 - 320//2,
                                           Config.Settings.get("SCREEN_HEIGHT")-40 - 120//2,
                                           color=(255, 255, 255), anchor_x="center", font_size=14)
        # waypoint
        self.hud_waypoint.init()
        # screen flash
        self.hud_flash_screen.init()
        # out of bounds warning
        self.hud_out_of_bounds.init()

    def bar_init(self, width: int, height: int, padding: int, color_front: Tuple[int, int, int] | Tuple[int, int, int, int],
                 color_back: Tuple[int, int, int] | Tuple[int, int, int, int], color_border: Tuple[int, int, int] | Tuple[int, int, int, int],
                 position: arcade.Point, list_pointer: list[arcade.SpriteSolidColor]) -> None:
        list_pointer.append(arcade.SpriteSolidColor(width, height, color_border))
        list_pointer.append(arcade.SpriteSolidColor(width - padding, height - padding, color_back))
        list_pointer.append(arcade.SpriteSolidColor(width - padding, height - padding, color_front))

        for e in list_pointer:
            EntityHandler.add(e, ObjectCategory.HUD)
            e.position = position

    def dash_bars_init(self) -> None:
        position: arcade.Point = (Config.Settings.get("SCREEN_WIDTH")//2, Config.Settings.get("SCREEN_HEIGHT")-88)
        x_offset: int = 80
        for i in range(Config.Constants.get("DASHES_MAX")):
            self.dash_bars.append(arcade.SpriteSolidColor(64, 24, (192, 192, 192, 192)))
            self.dash_bars[i].position = (position[0] + (i-1)*x_offset, position[1])
            EntityHandler.add(self.dash_bars[i], ObjectCategory.HUD)

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
        # inventory bar
        left_anchor = self.inventory_bar[active_idx].left
        self.inventory_bar[active_idx].width = max((self.player_ship.storage.inventory.capacity / self.player_ship.storage.inventory.max_capacity) * (160 - 8), 1)  # TODO tmp max fix
        self.inventory_bar[active_idx].left = left_anchor
        # dash bars
        for i in range(self.player_ship.dashes):
            self.dash_bars[i].color = (255, 255, 255)
        for i in range(self.player_ship.dashes, Config.Constants.get("DASHES_MAX")):
            self.dash_bars[i].color = (128, 128, 128)
        # waypoints
        self.hud_waypoint.process(delta)
        # screen flash
        self.hud_flash_screen.process(delta)
        # update quest text
        self.main_quest_text.text = self.main_quest_tracker.quest.get_progress_status_text()
        self.side_quest_text.text = self.side_quest_tracker.quest.get_progress_status_text()
        # out of bounds warning
        self.hud_out_of_bounds.process(delta)

    def draw(self) -> None:
        EntityHandler.draw(ObjectCategory.HUD)
        self.main_quest_text.draw()
        self.side_quest_text.draw()
        self.hud_out_of_bounds.draw()


if __name__ == '__main__':
    pass
