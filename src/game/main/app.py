
from typing import Tuple
import arcade

from src.game.main.background_drawer import BackgroundDrawer
from src.game.main.behaviors.finite_state_machine import FiniteStateMachine
from src.game.main.entities.enemies.enemy_ship import EnemyShip
from src.game.main.entities.player_ship import PlayerShip
from src.game.main.enums.input_mode import InputMode
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.gui.hud import HUD
from src.game.main.singletons.config import Config
from src.game.main.singletons.debug.console import Console
from src.game.main.singletons.debug.debug_critical import DebugCritical
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.singletons.input_handler import InputHandler
#tmp
from src.game.main.tempclasses.attacking_state import AttackingState
from src.game.main.tempclasses.calm_state import CalmState
from src.game.main.tempclasses.temp_wall import TempWall


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
        self.hud: HUD = None
        self.background: BackgroundDrawer = None


    def setup(self) -> None:
        # camera
        self.camera = arcade.Camera(self.width, self.height)
        self.hud_camera = arcade.Camera(self.width, self.height)
        # debug setup
        Console.init()
        DebugCritical.init()
        arcade.enable_timings(120) # TMP enable fps timings
        # player ship
        self.player_ship = PlayerShip((self.width/2, self.height/2))
        EntityHandler.add(self.player_ship, ObjectCategory.PLAYER)
        ###################################
        for i in range(2):
            enemy1 = EnemyShip((i*100, 300))
            EntityHandler.add(enemy1, ObjectCategory.ENEMIES)
            calm = CalmState(enemy1)
            behavior1 = FiniteStateMachine(calm, [AttackingState(enemy1, calm, self.player_ship, self.player_ship)], resumable=True)
            enemy1.add_behavior(behavior1)
        ###################################
        # hud init
        self.hud = HUD(self.player_ship)
        self.hud.init()
        # background
        self.background = BackgroundDrawer()
        self.background.init(self.player_ship)
        # TODO sprites loading class
        wall = TempWall()  # temporary
        wall.position = (600,500)  # temporary
        # initializing is only necessary if we check for collisions before drawing anything
        EntityHandler.initialize()
        EntityHandler.update_barrier_list()


    def on_update(self, delta_time: float) -> None:
        # arcade.print_timings() # TMP print fps timings
        # can update in custom order
        for category in ObjectCategory:
            EntityHandler.on_update(delta_time, category) # update everything in that list
        # move camera
        self.center_camera_on_player(delta_time)
        # debug update
        if InputHandler.key_binding_pressed("CONSOLE"):
            Console.draw_console_box = not Console.draw_console_box
            if Console.draw_console_box: InputHandler.mode = InputMode.CONSOLE
            else:                             InputHandler.mode = InputMode.INGAME
        if InputHandler.key_binding_pressed("DEBUG_PRINT"):
            DebugCritical.print = not DebugCritical.print
        Console.on_update()
        DebugCritical.on_update(self.camera)

        # hud
        self.hud.process(delta_time)
        # background
        self.background.process(delta_time)
        # always run this last
        InputHandler.clean()


    def on_draw(self) -> None:
        self.clear() # clean old
        # activate camera
        self.camera.use()
        # draw background
        self.background.draw()
        # draw sprites
        EntityHandler.draw(ObjectCategory.PROJECTILES)
        EntityHandler.draw(ObjectCategory.STATIC)
        EntityHandler.draw(ObjectCategory.MISC)
        EntityHandler.draw(ObjectCategory.ENEMIES)
        EntityHandler.draw(ObjectCategory.PLAYER)
        # activate hud camera
        self.hud_camera.use()
        EntityHandler.draw(ObjectCategory.HUD)
        # draw debug
        Console.draw()
        DebugCritical.draw()


    def center_camera_on_player(self, delta: float) -> None:
        center_x: float = self.player_ship.center_x - (self.camera.viewport_width / 2)
        center_y: float = self.player_ship.center_y - (self.camera.viewport_height / 2)

        center: Tuple[float, float] = (center_x, center_y)
        self.camera.move_to(center, App.CAMERA_MOVE_SPEED*delta)
        # self.camera.move(center) # TODO check how it works


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
