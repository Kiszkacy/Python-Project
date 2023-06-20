import arcade
from arcade import gui

from src.game.main.gui.views.fading_view import FadingView
import src.game.main.gui.views.menu as _


class Profile(FadingView):

    def __init__(self, window: arcade.Window) -> None:
        super(Profile, self).__init__(window)
        self.manager: gui.UIManager = arcade.gui.UIManager()
        self.layout: gui.UIBoxLayout = None
        self.level_text: gui.UILabel = None


    def setup(self) -> None:
        self.manager.enable()
        self.layout = gui.UIBoxLayout()

        # level information
        from src.game.main.singletons.player_statistics import PlayerStatistics
        PlayerStatistics.init()
        from src.game.main.level.progress_functions import calculate_level
        level: gui.UILabel = gui.UILabel(text=f"LEVEL {calculate_level(PlayerStatistics.stats['exp'])}", text_color=arcade.color.BLACK, font_size=50)
        self.layout.add(level)

        # create buttons
        button: gui.UIFlatButton = gui.UIFlatButton(text="Back", width=350, height=100)
        self.layout.add(button.with_space_around(bottom=40))
        button.on_click = self.on_back_button

        button = gui.UIFlatButton(text="Reset", width=350)
        self.layout.add(button.with_space_around(bottom=40))
        button.on_click = self.on_reset_button

        # NOTE: i think this magical code automatically centers whole ui ?
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.layout)
        )

    # ==============
    # BUTTON METHODS
    # ==============

    def on_back_button(self, event: gui.events.UIEvent) -> None:
        self.switch_view(_.Menu(self.window))

    def on_reset_button(self, event: gui.events.UIEvent) -> None:
        from src.game.main.singletons.player_statistics import PlayerStatistics
        PlayerStatistics.reset()

    # ==============

    def on_update(self, delta_time: float) -> None:
        super(Profile, self).on_update(delta_time)

    def on_show_view(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.CHARCOAL)

    def on_draw(self) -> None:
        self.clear() # clear old
        self.manager.draw()
        super(Profile, self).on_draw() # draw last so fade-in fade-out works


if __name__ == '__main__':
    pass
