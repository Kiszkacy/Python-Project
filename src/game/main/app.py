
import arcade

from src.game.main.gui.views.game_view import GameView
from src.game.main.gui.views.title_screen import TitleScreen
from src.game.main.gui.views.view import View
from src.game.main.singletons.config import Config
from src.game.main.singletons.input_handler import InputHandler


class App(arcade.Window): # TODO add minimal window size !!!

    def __init__(self, width: int = -1, height: int = -1, window_title: str = "Title") -> None:
        Config.load()
        if width == -1: width = Config.Settings.get("SCREEN_WIDTH")
        if height == -1: height = Config.Settings.get("SCREEN_HEIGHT") # TODO overwrite config resolution if provided ?
        super().__init__(width, height, window_title, vsync=False, gl_version=(4,4), resizable=True)
        arcade.set_background_color(arcade.csscolor.BLACK)

    def setup(self) -> None:
        starting_view: View = TitleScreen(self)
        starting_view.setup()
        self.show_view(starting_view)

    """
    NOTE: App on_update runs AFTER View on_update !!!
    """
    def on_update(self, delta_time: float) -> None:
        # always run this last
        InputHandler.clean()

    def on_draw(self) -> None:
        # NOTE: this cannot be called here anymore because its called AFTER view on_draw -> view must clean
        # self.clear() # clean old
        pass

    # ==== INPUT METHODS ====
    # TODO check if mouse button ids do not overlap with keyboard buttons
    # TODO note they do not but are in completely different module

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        InputHandler.mouse = (x, y)


    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        InputHandler.key_pressed[button] = True
        InputHandler.key_held[button] = True


    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int) -> None:
        InputHandler.key_released[button] = True
        InputHandler.key_held[button] = False


    def on_key_press(self, symbol: int, modifiers: int) -> None:
        InputHandler.key_pressed[symbol] = True
        InputHandler.key_held[symbol] = True


    def on_key_release(self, symbol: int, modifiers: int) -> None:
        InputHandler.key_released[symbol] = True
        InputHandler.key_held[symbol] = False


if __name__ == '__main__':
    pass
