import arcade

from src.game.main.gui.views.fading_view import FadingView
from src.game.main.gui.views.menu import Menu
from src.game.main.singletons.input_handler import InputHandler


class TitleScreen(FadingView):

    ANY_KEY_TEXT_TIME: float = 1.0 # TODO config?

    def __init__(self, window: arcade.Window) -> None:
        super(TitleScreen, self).__init__(window)
        self.title: arcade.Text = arcade.Text("TITLE TITLE TITLE", self.window.width/2, self.window.height-128,
                                              color=(255,255,255), anchor_x="center", font_size=48)
        self.any_key_text: arcade.Text = arcade.Text("Press any key to continue ...", self.window.width/2, self.window.height-128-64,
                                              color=(255,255,255), anchor_x="center", font_size=24)
        # SCRIPT VARS "PRIVATE"
        self.timer: float = TitleScreen.ANY_KEY_TEXT_TIME
        self.any_key_text_visibility: bool = False

    def setup(self) -> None:
        pass

    def on_update(self, delta_time: float) -> None:
        super(TitleScreen, self).on_update(delta_time)
        # update timer
        self.timer -= delta_time
        if self.timer <= 0.0:
            self.timer = TitleScreen.ANY_KEY_TEXT_TIME
            self.any_key_text_visibility = not self.any_key_text_visibility
        # check if anything pressed
        if any(val for val in InputHandler.key_pressed):
            self.switch_view(Menu(self.window))

    def on_resize(self, width: int, height: int) -> None: # NOTE: here update text/button position, size, widths etc
        # update text position if window resize
        self.title.position = (width / 2, height-128)
        self.any_key_text.position = (width / 2, height-128-64)

    def on_draw(self) -> None:
        self.clear() # clear everything
        self.title.draw()
        if self.any_key_text_visibility:
            self.any_key_text.draw()
        super(TitleScreen, self).on_draw() # call last for fade-in fade-out effect


if __name__ == '__main__':
    pass
