
import arcade
from src.entities.PlayerShip import PlayerShip
from src.singletons.EntityHandler import EntityHandler
from src.singletons.InputHandler import InputHandler
from src.auxilary.ObjectCategory import ObjectCategory

#tmp
from src.tempclasses.tempWall import TempWall

# TODO NOTES | self.update_rate <=> fps ?
# TODO NOTES | self.vsync
# TODO NOTES | self.samples
# TODO NOTES | self.gl_version
# TODO NOTES | self.antialiasing
# TODO NOTES | self.center_window
# TODO NOTES | self.fullscreen
# TODO NOTES | self.resizable
class App(arcade.Window):

    def __init__(self, width: int = 1280, height: int = 720, title: str = "Title") -> None:
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.csscolor.BLACK)
        self.playerShip: PlayerShip = None


    def setup(self) -> None:
        self.playerShip = PlayerShip()
        EntityHandler.add(self.playerShip, ObjectCategory.PLAYER)
        # initializing is only necessary if we check for collisions before drawing anything
        EntityHandler.initialize()
        # TODO sprites loading class

        wall = TempWall()  # temporary
        wall.position = (600,500)  # temporary


    def on_update(self, delta_time: float) -> None:
        # can update in custom order
        for category in ObjectCategory:
            EntityHandler.on_update(delta_time, category) # update everything in that list

        InputHandler.clean() # always run this last


    def on_draw(self) -> None:
        self.clear() # clean old
        # draw sprites
        EntityHandler.draw()
        # draw temporary gui
        arcade.draw_text(f"Cursor: {InputHandler.mouse[0]} {InputHandler.mouse[1]}", 0, 125, arcade.color.LIGHT_CYAN, font_size=25)
        arcade.draw_text(f"Space: {InputHandler.key_pressed[arcade.key.SPACE]}", 0, 75, arcade.color.LIGHT_CYAN, font_size=25)
        arcade.draw_text(f"Player angle: {self.playerShip.angle}", 0, 25, arcade.color.LIGHT_CYAN, font_size=25)

    # ==== INPUT METHODS ====
    # TODO check if mouse button ids do not overlap with keyboard buttons

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        InputHandler.mouse = (x, y)


    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        InputHandler.key_pressed[button] = True
        InputHandler.key_released[button] = False


    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int) -> None:
        InputHandler.key_released[button] = True
        InputHandler.key_pressed[button] = False


    def on_key_press(self, symbol: int, modifiers: int) -> None:
        InputHandler.key_pressed[symbol] = True
        InputHandler.key_released[symbol] = False


    def on_key_release(self, symbol: int, modifiers: int) -> None:
        InputHandler.key_released[symbol] = True
        InputHandler.key_pressed[symbol] = False


if __name__ == '__main__':
    pass
