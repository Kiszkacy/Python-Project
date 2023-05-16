import arcade
import arcade.gui as gui

from src.game.main.entities.enemies.enemy_basic import EnemyBasic
from src.game.main.gui.views.fading_view import FadingView
from src.game.main.singletons.config import Config
from src.game.main.singletons.input_handler import InputHandler
from src.game.main.util.random_walk import RandomWalk


class Settings(FadingView):

    def __init__(self, window: arcade.Window, parent: arcade.View,
                 background_color: tuple[int, int, int] = (0, 0, 0)) -> None:
        super(Settings, self).__init__(window)
        self.parent: arcade.View = parent
        self.background_color: tuple[int, int, int] = background_color
        self.manager: gui.UIManager = arcade.gui.UIManager()
        self.layout: gui.UIBoxLayout = None
        self.background_enemies: list[RandomWalk] = [RandomWalk(EnemyBasic((0, 0)), (window.width, window.height)) for _
                                                     in range(4)]
        self.scroll_offset = 0
        self.scroll_box: arcade.gui.UIAnchorWidget = None
        self.camera_gui = arcade.Camera(window.width, window.height)
        self.key_binding_waiting: str = None
        self.button_handle = None

    def setup(self) -> None:
        self.manager.enable()
        self.layout = gui.UIBoxLayout(space_between=20)

        title = gui.UILabel(text="SETTINGS", text_color=arcade.color.BLACK, font_size=30)
        self.layout.add(title)

        box_wrapper = gui.UIBoxLayout(vertical=False, space_between=20)
        left_box = gui.UIBoxLayout(space_between=10, align="left")
        right_box = gui.UIBoxLayout(space_between=10, align="right")

        self.layout.add(box_wrapper)
        box_wrapper.add(left_box)
        box_wrapper.add(right_box)

        # create buttons
        for key in Config.Keybindings.keys():
            box = gui.UIBoxLayout(vertical=False, space_between=200)
            left_box.add(gui.UILabel(text=key, text_color=arcade.color.BLACK, font_size=16))

            button = gui.UIFlatButton(text=Config.get_key_name(Config.Keybindings.get(key)[0]), width=200,
                                      height=30)
            right_box.add(button)
            button.on_click = self.get_key_bidding_button_method(key, button)

            # self.layout.add(box)

        # No saving for now
        # Exit buttons
        # exit_buttons = gui.UIBoxLayout(vertical=False, space_between=40)
        #
        # button = gui.UIFlatButton(text="Exit and Save", width=200)
        # exit_buttons.add(button.with_space_around(bottom=40, right=40))
        # button.on_click = self.on_click_exit_and_save_button

        button = gui.UIFlatButton(text="Exit", width=200)
        self.layout.add(button.with_space_around(bottom=40, left=40))
        button.on_click = self.on_click_exit_button

        # self.layout.add(exit_buttons)

        # NOTE: I think this magical code automatically centers whole ui ?
        self.scroll_box = arcade.gui.UIAnchorWidget(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.layout)

        self.manager.add(self.scroll_box)

    # ==============
    # BUTTON METHODS
    # ==============


    def get_key_bidding_button_method(self, key: str, button: gui.UIFlatButton):
        def on_click(event: gui.events.UIEvent):
            self.key_binding_waiting = key
            self.button_handle = button

        return on_click

    # TODO very TMP
    def on_click_exit_and_save_button(self, event: gui.events.UIEvent) -> None:
        from src.game.main.gui.views.pause import Pause
        from src.game.main.gui.views.menu import Menu
        if isinstance(self.parent, Pause):
            v = Pause(self.parent.game, self.window)
        else:
            v = Menu(self.window)
        v.setup()
        self.switch_view(v)

    # TODO very TMP
    def on_click_exit_button(self, event: gui.events.UIEvent) -> None:
        from src.game.main.gui.views.pause import Pause
        from src.game.main.gui.views.menu import Menu
        if isinstance(self.parent, Pause):
            v = Pause(self.parent.game, self.window)
        else:
            v = Menu(self.window)
        v.setup()
        self.switch_view(v)

    # ==============

    # TODO very TMP
    def on_update(self, delta_time: float) -> None:
        super(Settings, self).on_update(delta_time)
        for enemy in self.background_enemies: enemy.walk(delta_time)

        if InputHandler.key_binding_pressed("PAUSE"):
            self.on_click_exit_button(None)

        # arcade.set_viewport(0, self.window.width, self.scroll_offset, self.window.height + self.scroll_offset)
        if self.key_binding_waiting is not None:
            for key, val in InputHandler.key_pressed.items():
                if val:
                    Config.change_keybindings(self.key_binding_waiting, [key, *Config.Keybindings[self.key_binding_waiting][1:]])
                    self.key_binding_waiting = None
                    self.button_handle.text = Config.get_key_name(key)
                    self.button_handle = None
                    break

    def on_show_view(self):
        arcade.set_background_color(self.background_color)

    def on_draw(self) -> None:
        self.clear()  # clear old
        self.camera_gui.use()
        for enemy in self.background_enemies: enemy.body.draw()
        self.manager.draw()
        super(Settings, self).on_draw()  # draw last so fade-in fade-out works


if __name__ == '__main__':
    pass