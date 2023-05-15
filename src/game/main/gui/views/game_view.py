from typing import Tuple

import arcade

from src.game.main.entities.enemies.enemy import Enemy
from src.game.main.entities.enemies.enemy_basic import EnemyBasic
from src.game.main.entities.player_ship import PlayerShip
from src.game.main.enums.input_mode import InputMode
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.gui.ingame.hud import HUD
from src.game.main.gui.views.view import View
from src.game.main.sectors.sector_master import SectorMaster
from src.game.main.singletons.debug.console import Console
from src.game.main.singletons.debug.debug_critical import DebugCritical
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.singletons.input_handler import InputHandler
from src.game.main.tempclasses.temp_wall import TempWall
from src.game.main.vfx.background_drawer import BackgroundDrawer
from src.game.main.sectors.biomes import BiomeColorTheme


class GameView(View):

    CAMERA_MOVE_SPEED: float = 15.0 # TODO move to config

    def __init__(self, window: arcade.Window) -> None:
        super(GameView, self).__init__(window)
        self.player_ship: PlayerShip = None
        self.camera: arcade.Camera = None
        self.hud_camera: arcade.Camera = None
        self.hud: HUD = None
        self.background: BackgroundDrawer = None
        self.sector_master = None

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self) -> None:
        # camera
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.hud_camera = arcade.Camera(self.window.width, self.window.height)
        # debug setup
        Console.init()
        DebugCritical.init()
        arcade.enable_timings(120) # TMP enable fps timings
        # InputHandler.init() # should be called after loading config
        # player ship
        self.player_ship = PlayerShip((self.window.width/2, self.window.height/2))
        EntityHandler.add(self.player_ship, ObjectCategory.PLAYER)
        EntityHandler.player = self.player_ship
        # initializing is only necessary if we check for collisions before drawing anything
        EntityHandler.initialize()
        EntityHandler.player = self.player_ship
        # hud init
        self.hud = HUD(self.player_ship)
        self.hud.init()

        # generating sector
        self.sector_master = SectorMaster()
        self.sector_master.initialize()
        self.sector_master.current_sector.generate()

        # background
        self.background = BackgroundDrawer()
        self.background.init(self.player_ship, BiomeColorTheme[self.sector_master.current_sector.type])

        # TODO sprites loading class
        wall = TempWall()  # temporary
        wall.position = (600,500)  # temporary
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
            if Console.draw_console_box:    InputHandler.mode = InputMode.CONSOLE
            else:                           InputHandler.mode = InputMode.INGAME
        if InputHandler.key_binding_pressed("DEBUG_PRINT"):
            DebugCritical.print = not DebugCritical.print
        Console.on_update()
        DebugCritical.on_update(self.camera)

        # hud
        self.hud.process(delta_time)
        # background
        self.background.process(delta_time)

    def on_draw(self) -> None:
        self.clear() # clean old
        # activate camera
        self.camera.use()
        # draw background
        self.background.draw()
        # draw sprites
        # EntityHandler.draw(ObjectCategory.MISC)
        EntityHandler.draw(ObjectCategory.ITEMS)
        EntityHandler.draw(ObjectCategory.PROJECTILES)
        EntityHandler.draw(ObjectCategory.STATIC)
        EntityHandler.draw(ObjectCategory.NEUTRAL)
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
        self.camera.move_to(center, GameView.CAMERA_MOVE_SPEED*delta)
        # self.camera.move(center) # TODO check how it works

if __name__ == '__main__':
    pass
