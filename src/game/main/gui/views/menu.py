
import arcade
import arcade.gui as gui

from src.game.main.gui.views.fading_view import FadingView
from src.game.main.gui.views.profile_view import Profile
from src.game.main.gui.views.sector_map import SectorMap
from src.game.main.gui.views.settings import Settings


class Menu(FadingView):

    def __init__(self, window: arcade.Window) -> None:
        super(Menu, self).__init__(window)
        self.manager: gui.UIManager = arcade.gui.UIManager()
        self.layout: gui.UIBoxLayout = None

    def setup(self) -> None:
        self.manager.enable()
        self.layout = gui.UIBoxLayout()

        # create buttons
        button: gui.UIFlatButton = gui.UIFlatButton(text="Start", width=350, height=100)
        self.layout.add(button.with_space_around(bottom=40))
        button.on_click = self.on_click_start_button

        button = gui.UIFlatButton(text="Profile", width=350)
        self.layout.add(button.with_space_around(bottom=40))
        button.on_click = self.on_click_profile_button

        button = gui.UIFlatButton(text="Settings", width=350)
        self.layout.add(button.with_space_around(bottom=40))
        button.on_click = self.on_click_settings_button

        button = gui.UIFlatButton(text="Exit", width=350)
        self.layout.add(button.with_space_around(bottom=40))
        button.on_click = self.on_click_exit_button

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

    def on_click_start_button(self, event: gui.events.UIEvent) -> None:
        self.switch_view(SectorMap(self.window))

    def on_click_profile_button(self, event: gui.events.UIEvent) -> None:
        self.switch_view(Profile(self.window))

    def on_click_settings_button(self, event: gui.events.UIEvent) -> None:
        self.switch_view(Settings(self.window, self, arcade.color.GRAY))

    def on_click_exit_button(self, event: gui.events.UIEvent) -> None:
        arcade.exit()

    # ==============

    def on_update(self, delta_time: float) -> None:
        super(Menu, self).on_update(delta_time)

    def on_show_view(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.CHARCOAL)

    def on_draw(self) -> None:
        self.clear() # clear old
        self.manager.draw()
        super(Menu, self).on_draw() # draw last so fade-in fade-out works


if __name__ == '__main__':
    pass
