from __future__ import annotations

from time import sleep
from typing import Tuple, Optional
import arcade

from src.game.main.entities.player_ship import PlayerShip
from src.game.main.entities.formations.minable_asteroid import MinableAsteroid
from src.game.main.entities.formations.player_ship import PlayerSpawn
from src.game.main.enums.input_mode import InputMode
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.events.spawn_event import SpawnEvent
from src.game.main.gui.ingame.hud import HUD
from src.game.main.gui.views.death_view import DeathView
from src.game.main.gui.views.view import View
from src.game.main.quests.quest_gather_ore import QuestGatherOre
from src.game.main.quests.quest_tracker import QuestTracker
from src.game.main.sectors import biomes
from src.game.main.sectors.sector import Sector
from src.game.main.gui.views.pause import Pause
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.singletons.event_register import EventRegister
from src.game.main.singletons.game_save import GameSave
from src.game.main.singletons.input_handler import InputHandler
from src.game.main.particles.particles_handler import ParticlesHandler
from src.game.main.singletons.player_statistics import PlayerStatistics
from src.game.main.vfx.background_drawer import BackgroundDrawer
from src.game.main.sectors.biomes import BiomeColorTheme
from src.game.main.entities.formations.exit_portal import ExitPortal


class GameView(View):

    CAMERA_MOVE_SPEED: float = 15.0 # TODO move to config

    def __init__(self, window: arcade.Window, sector: Sector) -> None:
        super(GameView, self).__init__(window)
        self.player_ship: PlayerShip = None
        self.camera: arcade.Camera = None
        self.hud_camera: arcade.Camera = None
        self.hud: HUD = None
        self.background: BackgroundDrawer = None
        self.sector: Sector = sector
        self.particle_handler: ParticlesHandler = None
        self.exit_portal_spawned: bool = False
        self.exit_portal: ExitPortal = None
        self.first_load: bool = True

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self) -> None:
        if self.first_load:
            # camera
            self.camera = arcade.Camera(self.window.width, self.window.height)
            self.hud_camera = arcade.Camera(self.window.width, self.window.height)
            # particle handler init
            self.particle_handler = ParticlesHandler(self.window.ctx, self.camera)
            self.particle_handler.setup()
            # debug setup
            # Console.init()
            # DebugCritical.init()
            PlayerStatistics.init()
            arcade.enable_timings(120) # TMP enable fps timings
            # initializing is only necessary if we check for collisions before drawing anything
            GameSave.innit()
            # generating sector map
            # self.sector_master: SectorMaster = SectorMaster()
            # self.sector_master.initialize()

            # player ship
            player_spawn: PlayerSpawn = PlayerSpawn()
            self.player_ship = player_spawn.entities[0][0]
            EntityHandler.player = self.player_ship

            self.sector.pre_generate()

            EntityHandler.initialize()
            EntityHandler.bucket_init(self.sector.width, self.sector.height) # bucket_init after pregenerate before generate !

            self.sector.generate()

            # setup quests
            main_quest: QuestTracker = QuestTracker(self.sector.main_quest)
            main_quest.setup()
            side_quest: QuestTracker = QuestTracker(self.sector.side_quest)
            side_quest.setup()

            # add some asteroids if mining quest
            if isinstance(self.sector.side_quest, QuestGatherOre):  # TODO very ugly
                for i in range(40):
                    asteroid: MinableAsteroid = MinableAsteroid()
                    pos = self.sector.find_empty_space(asteroid.width, asteroid.height, 10)
                    if pos is None: continue
                    asteroid.place(pos, ObjectCategory.NEUTRAL, bucketable=True)
                    print("asteroid")

            # spawn player
            pos: Optional[arcade.Point] = None
            while pos is None:
                pos = self.sector.find_empty_space(player_spawn.width, player_spawn.height, 1000, offset=(5000, 5000, 5000, 5000)) # TODO constant
            player_spawn.place(pos, ObjectCategory.PLAYER, bucketable=True)
            self.player_ship = player_spawn.entities[0][0]
            EntityHandler.player = self.player_ship

            # hud init
            self.hud = HUD(main_quest, side_quest)
            self.hud.init()

            # background
            self.background = BackgroundDrawer()
            self.background.init(self.player_ship, BiomeColorTheme[self.sector.type])

            self.first_load = False
        else:
            PlayerStatistics.player_alive = True
            # clear portal things
            self.exit_portal_spawned = False
            self.exit_portal = None
            # clear entity handler
            EntityHandler.categorized = [arcade.SpriteList() for _ in ObjectCategory]

            # player ship
            player_spawn: PlayerSpawn = PlayerSpawn()
            self.player_ship = player_spawn.entities[0][0]
            EntityHandler.player = self.player_ship

            # sector pregenerate
            self.sector.pre_generate()

            # recreate buckets
            EntityHandler.bucket_init(self.sector.width, self.sector.height) # bucket_init after pregenerate before generate !

            # generate sector
            self.sector.generate()

            # setup quests
            main_quest: QuestTracker = QuestTracker(self.sector.main_quest)
            main_quest.setup()
            side_quest: QuestTracker = QuestTracker(self.sector.side_quest)
            side_quest.setup()

            # add some asteroids if mining quest
            if isinstance(self.sector.side_quest, QuestGatherOre): # TODO very ugly
                for i in range(40):
                    asteroid: MinableAsteroid = MinableAsteroid()
                    pos = self.sector.find_empty_space(asteroid.width, asteroid.height, 10)
                    if pos is None: continue
                    asteroid.place(pos, ObjectCategory.NEUTRAL, bucketable=True)
                    print("asteroid")

            # spawn player
            pos: Optional[arcade.Point] = None
            while pos is None:
                pos = self.sector.find_empty_space(player_spawn.width, player_spawn.height, 1000, offset=(5000, 5000, 5000, 5000)) # TODO constant
            player_spawn.place(pos, ObjectCategory.PLAYER, bucketable=True)
            self.player_ship = player_spawn.entities[0][0]
            EntityHandler.player = self.player_ship

            # hud init
            self.hud = HUD(main_quest, side_quest)
            self.hud.init()

            # background
            self.background = BackgroundDrawer()
            self.background.init(self.player_ship, BiomeColorTheme[self.sector.type])


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
            sector_type: biomes.Biome = self.sector.type
            self.switch_view(DeathView(self.window, biomes.get_biome_color_theme(sector_type)))
            return

        if InputHandler.key_binding_pressed("PAUSE"):
            self.switch_view(Pause(self, self.window))

        # exiting sector
        if self.exit_portal is not None and self.exit_portal_spawned and self.exit_portal.entities[0][0].used:
            print("Exit portal and things", self.exit_portal_spawned, self.sector.main_quest.is_completed())
            from src.game.main.gui.views.sector_map import SectorMap
            self.switch_view(SectorMap(self.window))

        # hud
        self.hud.process(delta_time)
        # particles
        self.particle_handler.process(delta_time)
        # background
        self.background.process(delta_time)
        # check if main quest is done
        if not self.exit_portal_spawned and self.sector.main_quest.is_completed():
            exit_portal: ExitPortal = ExitPortal()
            pos: Optional[arcade.Point] = None
            while pos is None:
                pos = self.sector.find_empty_space(exit_portal.width, exit_portal.height, 1000)
            exit_portal.place(pos, ObjectCategory.FRIENDLY, bucketable=True)
            EventRegister.register_new(SpawnEvent(exit_portal.entities[0][0], pos))
            self.exit_portal = exit_portal
            self.exit_portal_spawned = True

    def on_draw(self) -> None:
        self.clear() # clean old
        # activate camera
        self.camera.use()
        # draw background
        self.background.draw()
        # draw particles
        self.particle_handler.draw()
        # draw sprites
        EntityHandler.draw(ObjectCategory.ITEMS)
        EntityHandler.draw(ObjectCategory.PROJECTILES)
        EntityHandler.draw(ObjectCategory.STATIC)
        EntityHandler.draw(ObjectCategory.FRIENDLY)
        EntityHandler.draw(ObjectCategory.NEUTRAL)
        EntityHandler.draw(ObjectCategory.ENEMIES)
        EntityHandler.draw(ObjectCategory.PLAYER)
        EntityHandler.draw(ObjectCategory.MISC)
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
