import arcade

from src.game.main.entities.player_ship import PlayerShip
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.singletons.config import Config
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.singletons.input_handler import InputHandler
from src.game.main.singletons.singleton import Singleton
from src.game.main.util.math import magnitude


class DebugCritical(metaclass=Singleton):
    
    # ct = critical_text = bottom left debug lines
    ct_font_size: int = 20
    ct_screen_offset: int = 15
    ct_line_offset: int = 30
    ct_line_count: int = 10
    ct: list[arcade.Text] = []
    print: bool = False

    @staticmethod
    def init() -> None:
        DebugCritical.ct = [arcade.Text(f"DEBUG CRITICAL TEXT LINE {i}",
                              start_x=DebugCritical.ct_screen_offset,
                              start_y=DebugCritical.ct_screen_offset + DebugCritical.ct_line_offset * i,
                              color=arcade.color.WHITE,
                              font_size=DebugCritical.ct_font_size)
                              for i in range(DebugCritical.ct_line_count)]

    @staticmethod
    def on_update(camera: arcade.Camera) -> None:
        # update critical text
        player: PlayerShip = EntityHandler.categorized[ObjectCategory.PLAYER][0]  # TODO ugly
        if player is not None:
            texts: list[str] = [f"FPS: {arcade.get_fps()}",
                                f"Cursor: {InputHandler.mouse[0]} {InputHandler.mouse[1]}",
                                f"Player: {player.position}",
                                f"Camera: {camera.position[0] + Config.Settings.get('SCREEN_WIDTH') / 2.0, camera.position[1] + Config.Settings.get('SCREEN_HEIGHT') / 2.0}",
                                f"Active weapon idx: {player.weapon_idx}",
                                f"Space: {InputHandler.key_pressed.get(arcade.key.SPACE, False)}",
                                f"Player angle: {player.angle}",
                                f"Player power: {player.power}",
                                f"Player velocity: {player.velocity}",
                                f"Player speed: {magnitude(player.velocity)}"]
            for idx, line in enumerate(DebugCritical.ct):
                line.text = texts[idx]


    @staticmethod
    def draw() -> None:
        if DebugCritical.print:
            for text in DebugCritical.ct:
                text.draw()


if __name__ == '__main__':
    pass
