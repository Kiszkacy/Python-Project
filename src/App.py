
import arcade
from src.entities.PlayerShip import PlayerShip
from src.singletons.EntityHandler import EntityHandler
from src.singletons.InputHandler import InputHandler
from src.auxilary.ObjectCategory import ObjectCategory
from src.util.VectorMath import length
from src.singletons.Config import Config

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
        arcade.enable_timings(120) # TMP enable fps timings
        Config.load_config()
        self.playerShip = PlayerShip((self.width/2, self.height/2))
        EntityHandler.add(self.playerShip, ObjectCategory.PLAYER)
        # initializing is only necessary if we check for collisions before drawing anything
        EntityHandler.initialize()
        # TODO sprites loading class

        wall = TempWall()  # temporary
        wall.position = (600,500)  # temporary


    def on_update(self, delta_time: float) -> None:
        arcade.print_timings() # TMP print fps timings
        # can update in custom order
        for category in ObjectCategory:
            EntityHandler.on_update(delta_time, category) # update everything in that list

        InputHandler.clean() # always run this last


    def on_draw(self) -> None:
        self.clear() # clean old
        # draw sprites
        EntityHandler.draw()
        # draw temporary gui
        arcade.draw_text(f"FPS: {arcade.get_fps()}", 15, 225, arcade.color.LIGHT_CYAN, font_size=20)
        arcade.draw_text(f"Cursor: {InputHandler.mouse[0]} {InputHandler.mouse[1]}", 15, 195, arcade.color.LIGHT_CYAN, font_size=20)
        arcade.draw_text(f"Active weapon idx: {self.playerShip.weapon_idx}", 15, 165, arcade.color.LIGHT_CYAN, font_size=20)
        arcade.draw_text(f"Space: {InputHandler.key_pressed[arcade.key.SPACE]}", 15, 135, arcade.color.LIGHT_CYAN, font_size=20)
        arcade.draw_text(f"Player angle: {self.playerShip.angle}", 15, 105, arcade.color.LIGHT_CYAN, font_size=20)
        arcade.draw_text(f"Player power: {self.playerShip.power}", 15, 75, arcade.color.LIGHT_CYAN, font_size=20)
        arcade.draw_text(f"Player velocity: {self.playerShip.velocity}", 15, 45, arcade.color.LIGHT_CYAN, font_size=20)
        arcade.draw_text(f"Player speed: {length(self.playerShip.velocity)}", 15, 15, arcade.color.LIGHT_CYAN, font_size=20)

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
