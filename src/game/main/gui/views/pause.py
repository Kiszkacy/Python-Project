import arcade
import arcade.gui as gui

from src.game.main.entities.enemies.enemy_basic import EnemyBasic
from src.game.main.gui.views.fading_view import FadingView
from src.game.main.gui.views.settings import Settings
from src.game.main.singletons.input_handler import InputHandler
from src.game.main.sectors import biomes
from src.game.main.util.random_walk import RandomWalk

class Pause(FadingView):

    def __init__(self, game, window: arcade.Window) -> None:
        super(Pause, self).__init__(window)
        self.game = game
        self.manager: gui.UIManager = arcade.gui.UIManager()
        self.layout: gui.UIBoxLayout = None
        self.background_enemies: list[RandomWalk] = [RandomWalk(EnemyBasic((0,0)), (window.width, window.height)) for _ in range(4)]

    def setup(self) -> None:
        self.manager.enable()
        self.layout = gui.UIBoxLayout()

        title = gui.UILabel(text="PAUSED", text_color=arcade.color.BLACK, font_size=50)
        self.layout.add(title)
        # create buttons
        button: gui.UIFlatButton = gui.UIFlatButton(text="Continue", width=350, height=100)
        self.layout.add(button.with_space_around(bottom=40))
        button.on_click = self.on_click_continue_button

        button = gui.UIFlatButton(text="Settings", width=350)
        self.layout.add(button.with_space_around(bottom=40))
        button.on_click = self.on_click_settings_button

        button = gui.UIFlatButton(text="Exit", width=350)
        self.layout.add(button.with_space_around(bottom=40))
        button.on_click = self.on_click_exit_button

        # NOTE: I think this magical code automatically centers whole ui ?
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.layout)
        )

        # ==============
        # BUTTON METHODS
        # ==============

    def on_click_continue_button(self, event: gui.events.UIEvent) -> None:
        self.window.show_view(self.game)

    def on_click_settings_button(self, event: gui.events.UIEvent) -> None:
        sector_type: biomes.Biome = self.game.sector_master.current_sector.type
        background_colour: tuple[int, int, int] = biomes.get_biome_color_theme(sector_type)
        self.switch_view(Settings(self.window, self, background_colour))

    def on_click_exit_button(self, event: gui.events.UIEvent) -> None:
        arcade.exit()

        # ==============

    def on_update(self, delta_time: float) -> None:
        super(Pause, self).on_update(delta_time)
        for enemy in self.background_enemies: enemy.walk(delta_time)
        if InputHandler.key_binding_pressed("PAUSE"):
            self.window.show_view(self.game)

    def on_show_view(self):
        sector_type: biomes.Biome = self.game.sector_master.current_sector.type
        arcade.set_background_color(biomes.get_biome_color_theme(sector_type))

    def on_draw(self) -> None:
        self.clear()  # clear old
        for enemy in self.background_enemies: enemy.body.draw()
        self.manager.draw()
        super(Pause, self).on_draw()  # draw last so fade-in fade-out works