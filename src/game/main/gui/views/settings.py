import arcade

from src.game.main.gui.views.view import View


class Settings(View):

    def __init__(self, window: arcade.Window) -> None:
        super(Settings, self).__init__(window)

    def setup(self) -> None:
        pass


if __name__ == '__main__':
    pass
