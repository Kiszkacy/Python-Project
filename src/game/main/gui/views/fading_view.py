from typing import Optional, Type

import arcade

from src.game.main.gui.views.view import View


class FadingView(View):
    def __init__(self, window: arcade.Window, fade_rate: int = 10):
        super().__init__(window)
        self.fade_out: Optional[int] = None
        self.fade_in: Optional[int] = 255
        self.fade_rate: int = fade_rate
        self.next_view: Optional[View] = None

    def on_update(self, delta_time: float) -> None:
        self.update_fade()

    def on_draw(self) -> None:
        self.draw_fading()

    def switch_view(self, to: View) -> None:
        self.next_view = to
        if self.fade_out is None: self.fade_out = 0 # this controls when view will be switched

    def update_fade(self) -> None:
        if self.fade_out is not None:
            self.fade_out += self.fade_rate
            if self.fade_out is not None and self.fade_out > 255 and self.next_view is not None:
                self.next_view.setup()
                self.window.show_view(self.next_view)

        if self.fade_in is not None:
            self.fade_in -= self.fade_rate
            if self.fade_in <= 0: self.fade_in = None

    def draw_fading(self):
        if self.fade_out is not None:
            arcade.draw_rectangle_filled(self.window.width / 2, self.window.height / 2,
                                         self.window.width, self.window.height,
                                         (0, 0, 0, self.fade_out))

        if self.fade_in is not None:
            arcade.draw_rectangle_filled(self.window.width / 2, self.window.height / 2,
                                         self.window.width, self.window.height,
                                         (0, 0, 0, self.fade_in))


if __name__ == '__main__':
    pass
