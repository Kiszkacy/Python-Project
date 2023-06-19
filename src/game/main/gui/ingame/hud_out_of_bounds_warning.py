
import arcade

from src.game.main.entities.player_ship import PlayerShip
from src.game.main.interfaces.processable import Processable
from src.game.main.singletons.config import Config
from src.game.main.singletons.entity_handler import EntityHandler


class HUDOutOfBounds(Processable):

    CYCLE_LENGTH: float = 0.5  # TODO config

    def __init__(self) -> None:
        self.text: arcade.Text = None
        self.subtext: arcade.Text = None
        self.active: bool = False
        # SCRIPT VARS "PRIVATE"
        self.timer: float = HUDOutOfBounds.CYCLE_LENGTH
        self.frequency = HUDOutOfBounds.CYCLE_LENGTH
        self.visible: bool = True

    def init(self) -> None:
        self.text = arcade.Text("WARNING",
                                Config.Settings.get("SCREEN_WIDTH") // 2,
                                Config.Settings.get("SCREEN_HEIGHT") // 2 - 120,
                                color=(255, 0, 0), anchor_x="center", font_size=24)
        self.subtext = arcade.Text("TURN BACK",
                                   Config.Settings.get("SCREEN_WIDTH") // 2,
                                   Config.Settings.get("SCREEN_HEIGHT") // 2 - 80,
                                   color=(255, 0, 0), anchor_x="center", font_size=18)

    def process(self, delta: float) -> None:
        player_ship: PlayerShip = EntityHandler.player
        bucket_x: int = player_ship.bucket_x_idx
        bucket_y: int = player_ship.bucket_y_idx
        buffer_size: int = Config.Constants.get("OUT_OF_BOUNDS_WARNING_BUCKET_BUFFER")
        self.active = bucket_x <= buffer_size or bucket_x >= EntityHandler.bucket_x_count-buffer_size\
                      or bucket_y <= buffer_size or bucket_y >= EntityHandler.bucket_y_count-buffer_size
        # update frequency and timer if active
        if not self.active: return

        bucket_size: int = Config.Constants.get("BUCKET_SIZE")
        x: float = player_ship.position[0]
        y: float = player_ship.position[1]
        self.update_frequency(max(0.1, min(x / (bucket_size*buffer_size), y / (bucket_size*buffer_size),
                                           (EntityHandler.bucket_x_count*bucket_size-x) / (bucket_size*buffer_size),
                                           (EntityHandler.bucket_y_count*bucket_size-y) / (bucket_size*buffer_size))))

        self.timer -= delta
        if self.timer <= 0.0:
            self.timer = self.frequency
            self.visible = not self.visible

    def draw(self) -> None:
        if not self.active or not self.visible: return
        self.text.draw()
        self.subtext.draw()

    def update_frequency(self, multiplier: float) -> None:
        self.frequency = HUDOutOfBounds.CYCLE_LENGTH * multiplier


if __name__ == '__main__':
    pass
