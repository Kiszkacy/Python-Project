from __future__ import annotations

from time import sleep
from typing import Tuple
import arcade

from src.game.main.entities.player_ship import PlayerShip
from src.game.main.enums.input_mode import InputMode
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.gui.ingame.hud import HUD
from src.game.main.gui.views.death_view import DeathView
from src.game.main.gui.views.view import View
from src.game.main.quests.quest_tracker import QuestTracker
from src.game.main.sectors import biomes
from src.game.main.sectors.sector_master import SectorMaster
from src.game.main.gui.views.pause import Pause
from src.game.main.singletons.debug.console import Console
from src.game.main.singletons.debug.debug_critical import DebugCritical
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.singletons.input_handler import InputHandler
from src.game.main.particles.particles_handler import ParticlesHandler
from src.game.main.singletons.player_statistics import PlayerStatistics
from src.game.main.tempclasses.temp_wall import TempWall
from src.game.main.vfx.background_drawer import BackgroundDrawer
from src.game.main.sectors.biomes import BiomeColorTheme

from multiprocessing import Pool


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
        self.particle_handler: ParticlesHandler = None
        self.main_quest: QuestTracker = None
        self.side_quest: QuestTracker = None

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self) -> None:
        # camera
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.hud_camera = arcade.Camera(self.window.width, self.window.height)
        # particle handler init
        self.particle_handler = ParticlesHandler(self.window.ctx, self.camera)
        self.particle_handler.setup()
        # debug setup
        # Console.init()
        # DebugCritical.init()
        PlayerStatistics.innit()
        arcade.enable_timings(120) # TMP enable fps timings
        # initializing is only necessary if we check for collisions before drawing anything
        EntityHandler.initialize()
        EntityHandler.player = self.player_ship

        # generating sector
        self.sector_master = SectorMaster()
        self.sector_master.initialize()
        self.sector_master.current_sector.pre_generate()
        EntityHandler.bucket_init(self.sector_master.current_sector.width, self.sector_master.current_sector.height) # bucket_init after pregenerate before generate !

        # player ship
        self.player_ship = PlayerShip((self.window.width/2, self.window.height/2))
        EntityHandler.add(self.player_ship, ObjectCategory.PLAYER, True)
        EntityHandler.player = self.player_ship

        self.sector_master.current_sector.generate()

        # setup quests
        self.main_quest = QuestTracker(self.sector_master.current_sector.main_quest)
        self.main_quest.setup()
        self.side_quest = QuestTracker(self.sector_master.current_sector.side_quest)
        self.side_quest.setup()

        # hud init
        self.hud = HUD(self.player_ship, self.main_quest, self.side_quest)
        self.hud.init()

        # background
        self.background = BackgroundDrawer()
        self.background.init(self.player_ship, BiomeColorTheme[self.sector_master.current_sector.type])

        # wall = TempWall()  # temporary
        # wall.position = (600,500)  # temporary
        # EntityHandler.update_barrier_list()

    def on_update(self, delta_time: float) -> None:
        # arcade.print_timings() # TMP print fps timings
        # can update in custom order
        for category in ObjectCategory:
            # EntityHandler.update(delta_time, category) # update everything in that list
            if category == ObjectCategory.HUD or category == ObjectCategory.PLAYER: # update everything if player or hud
                EntityHandler.update(delta_time, category)
            else:
                EntityHandler.update_close_buckets(delta_time, category)
        # move camera
        self.center_camera_on_player(delta_time)

        if not PlayerStatistics.player_alive:
            sector_type: biomes.Biome = self.sector_master.current_sector.type
            self.switch_view(DeathView(self.window, biomes.get_biome_color_theme(sector_type)))
            return

        if InputHandler.key_binding_pressed("PAUSE"):
            self.switch_view(Pause(self, self.window))
        # debug update
        # if InputHandler.key_binding_pressed("CONSOLE"):
        #     Console.draw_console_box = not Console.draw_console_box
        #     if Console.draw_console_box:    InputHandler.mode = InputMode.CONSOLE
        #     else:                           InputHandler.mode = InputMode.INGAME
        # if InputHandler.key_binding_pressed("DEBUG_PRINT"):
        #     DebugCritical.print = not DebugCritical.print
        # Console.on_update()
        # DebugCritical.on_update(self.camera)

        # hud
        self.hud.process(delta_time)

        # particles
        self.particle_handler.process(delta_time)

        # background
        self.background.process(delta_time)

    def on_draw(self) -> None:
        self.clear() # clean old
        # activate camera
        self.camera.use()
        # draw background
        self.background.draw()
        # draw particles
        self.particle_handler.draw()
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
        self.hud.draw()
        # draw debug
        # Console.draw()
        # DebugCritical.draw()

    def center_camera_on_player(self, delta: float) -> None:
        center_x: float = self.player_ship.center_x - (self.camera.viewport_width / 2)
        center_y: float = self.player_ship.center_y - (self.camera.viewport_height / 2)

        center: Tuple[float, float] = (center_x, center_y)
        self.camera.move_to(center, GameView.CAMERA_MOVE_SPEED*delta)
        # self.camera.move(center) # TODO check how it works


if __name__ == '__main__':
    pass
