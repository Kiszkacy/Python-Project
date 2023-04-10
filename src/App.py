
from typing import Tuple
import arcade
from src.auxilary.InputMode import InputMode
from src.entities.PlayerShip import PlayerShip
from src.gui.ingame_hud import IngameHUD
from src.singletons.EntityHandler import EntityHandler
from src.singletons.InputHandler import InputHandler
from src.auxilary.ObjectCategory import ObjectCategory
from src.singletons.debug_console import DebugConsole
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

    CAMERA_MOVE_SPEED: float = 15.0

    def __init__(self, width: int = -1, height: int = -1, title: str = "Title") -> None:
        Config.load()
        if width == -1: width = Config.Settings.get("SCREEN_WIDTH")
        if height == -1: height = Config.Settings.get("SCREEN_HEIGHT") # TODO overwrite config resolution if provided ?
        super().__init__(width, height, title, vsync=False, gl_version=(4,4))
        arcade.set_background_color(arcade.csscolor.BLACK)
        self.player_ship: PlayerShip = None
        self.camera: arcade.Camera = None
        self.hud_camera: arcade.Camera = None
        self.hud: IngameHUD = None


    def setup(self) -> None:
        # camera
        self.camera = arcade.Camera(self.width, self.height)
        self.hud_camera = arcade.Camera(self.width, self.height)
        # debug setup
        DebugConsole.init()
        arcade.enable_timings(120) # TMP enable fps timings
        # InputHandler.init() # should be called after loading config
        self.player_ship = PlayerShip((self.width/2, self.height/2))
        EntityHandler.add(self.player_ship, ObjectCategory.PLAYER)
        # initializing is only necessary if we check for collisions before drawing anything
        EntityHandler.initialize()
        # hud init
        self.hud = IngameHUD(self.player_ship)
        self.hud.init()
        # TODO sprites loading class
        wall = TempWall()  # temporary
        wall.position = (600,500)  # temporary


    def on_update(self, delta_time: float) -> None:
        # arcade.print_timings() # TMP print fps timings
        # can update in custom order
        for category in ObjectCategory:
            EntityHandler.on_update(delta_time, category) # update everything in that list

        # move camera
        self.center_camera_on_player(delta_time)

        # debug console update
        if InputHandler.key_binding_pressed("CONSOLE"):
            DebugConsole.draw_console_box = not DebugConsole.draw_console_box
            if DebugConsole.draw_console_box: InputHandler.mode = InputMode.CONSOLE
            else:                             InputHandler.mode = InputMode.INGAME
        if InputHandler.key_binding_pressed("DEBUG_PRINT"):
            DebugConsole.draw_critical = not DebugConsole.draw_critical
        DebugConsole.on_update(self.camera)

        self.hud.process(delta_time)
        # always run this last
        InputHandler.clean()


    def on_draw(self) -> None:
        self.clear() # clean old
        # activate camera
        self.camera.use()
        # draw sprites
        EntityHandler.draw(ObjectCategory.PROJECTILES)
        EntityHandler.draw(ObjectCategory.STATIC)
        EntityHandler.draw(ObjectCategory.MISC)
        EntityHandler.draw(ObjectCategory.ENEMIES)
        EntityHandler.draw(ObjectCategory.PLAYER)
        # activate hud camera
        self.hud_camera.use()
        EntityHandler.draw(ObjectCategory.HUD)
        # draw debug info
        DebugConsole.draw()


    def center_camera_on_player(self, delta: float) -> None:
        center_x: float = self.player_ship.center_x - (self.camera.viewport_width / 2)
        center_y: float = self.player_ship.center_y - (self.camera.viewport_height / 2)

        center: Tuple[float, float] = (center_x, center_y)
        self.camera.move_to(center, App.CAMERA_MOVE_SPEED*delta)
        # self.camera.move(center) # TODO check how it works


    # ==== INPUT METHODS ====
    # TODO check if mouse button ids do not overlap with keyboard buttons

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
