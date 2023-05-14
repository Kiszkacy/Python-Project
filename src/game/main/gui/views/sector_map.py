import arcade

from src.game.main.gui.views.game_view import GameView
from src.game.main.gui.views.view import View
from src.game.main.singletons.input_handler import InputHandler


class SectorMap(View):

    def __init__(self, window: arcade.Window) -> None:
        super(SectorMap, self).__init__(window)

    def setup(self) -> None:
        pass

    def on_update(self, delta_time: float) -> None:
        # check if anything pressed
        if any(val for val in InputHandler.key_pressed):
            print("SWITCH")
            self.switch_view(GameView(self.window))


if __name__ == '__main__':
    pass
