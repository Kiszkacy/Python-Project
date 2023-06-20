import arcade
import arcade.gui as gui

from src.game.main.entities.enemies.enemy_basic import EnemyBasic
from src.game.main.gui.views.fading_view import FadingView
from src.game.main.gui.views.settings import Settings
from src.game.main.singletons.input_handler import InputHandler
from src.game.main.sectors import biomes
from src.game.main.singletons.player_statistics import PlayerStatistics
from src.game.main.util.on_exit import on_exit
from src.game.main.util.random_walk import RandomWalk

class DeathView(FadingView):

    def __init__(self, window: arcade.Window, background_color: tuple[int, int, int] = (0, 0, 0)) -> None:
        super(DeathView, self).__init__(window)
        self.background_color = background_color
        self.manager: gui.UIManager = arcade.gui.UIManager()
        self.layout: gui.UIBoxLayout = None
        self.background_enemies: list[RandomWalk] = [RandomWalk(EnemyBasic((0,0)), (window.width, window.height)) for _ in range(4)]

    def setup(self) -> None:
        self.manager.enable()
        self.layout = gui.UIBoxLayout()

        title = gui.UILabel(text="You are dead", text_color=arcade.color.BLACK, font_size=50)
        self.layout.add(title)

        box_wrapper = gui.UIBoxLayout(vertical=False, space_between=20)
        left_box = gui.UIBoxLayout(space_between=10, align="left")
        right_box = gui.UIBoxLayout(space_between=10, align="right")
        self.layout.add(box_wrapper)
        box_wrapper.add(left_box)
        box_wrapper.add(right_box)

        # create buttons
        for stats_name, stats_value in PlayerStatistics.stats.items():
            stats_representation = stats_name.capitalize().replace("_", " ")
            left_box.add(gui.UILabel(text=stats_representation, text_color=arcade.color.BLACK, font_size=20))
            right_box.add(gui.UILabel(text=str(stats_value), text_color=arcade.color.BLACK, font_size=20))

        # button = gui.UIFlatButton(text="Settings", width=350)
        # self.layout.add(button.with_space_around(bottom=40))
        # button.on_click = self.on_click_settings_button
        v_box = gui.UIBoxLayout(vertical=False, space_between=20)
        self.layout.add(v_box)

        button: gui.UIFlatButton = gui.UIFlatButton(text="Try again", width=350)
        v_box.add(button.with_space_around(bottom=40))
        button.on_click = self.on_click_continue_button

        button = gui.UIFlatButton(text="Exit", width=350)
        v_box.add(button.with_space_around(bottom=40))
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

    # starts new game
    def on_click_continue_button(self, event: gui.events.UIEvent) -> None:
        from src.game.main.gui.views.sector_map import SectorMap
        self.switch_view(SectorMap(self.window))

    # def on_click_settings_button(self, event: gui.events.UIEvent) -> None:
    #     self.switch_view(Settings(self.window, self, self.background_color))

    def on_click_exit_button(self, event: gui.events.UIEvent) -> None:
        on_exit()
        arcade.exit()

    # ==============

    def on_update(self, delta_time: float) -> None:
        super(DeathView, self).on_update(delta_time)
        for enemy in self.background_enemies: enemy.walk(delta_time)

    def on_show_view(self):
        arcade.set_background_color(self.background_color)

    def on_draw(self) -> None:
        self.clear()  # clear old
        for enemy in self.background_enemies: enemy.body.draw()
        self.manager.draw()
        super(DeathView, self).on_draw()  # draw last so fade-in fade-out works
