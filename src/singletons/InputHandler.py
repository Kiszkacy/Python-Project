
import arcade
from src.singletons.Singleton import Singleton
from src.singletons.Config import Config


class InputHandler(metaclass=Singleton):

    mouse: arcade.Point = (0,0)
    key_pressed: dict = {} # TODO fix me later please ;-;
    key_released: dict = {} # TODO fix me later please ;-;

    @staticmethod
    def clean() -> None:
        for key in InputHandler.key_released.keys():
            InputHandler.key_released[key] = False

    @staticmethod
    def key_binding_pressed(name: str) -> bool:
        codes: list[int] = Config.Keybindings[name]
        return True in [InputHandler.key_pressed.get(code, "False") for code in codes]


if __name__ == '__main__':
    pass
