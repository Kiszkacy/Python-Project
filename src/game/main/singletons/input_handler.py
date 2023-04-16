
import arcade

from src.game.main.enums.input_mode import InputMode
from src.game.main.singletons.config import Config
from src.game.main.singletons.singleton import Singleton


class InputHandler(metaclass=Singleton):

    mouse: arcade.Point = (0,0)
    key_pressed: dict = {}
    key_held: dict = {}
    key_released: dict = {}
    mode: InputMode = InputMode.INGAME # TODO change in future when menu is added to InputMode.MENU

    @staticmethod
    def clean() -> None:
        for key in InputHandler.key_released.keys():
            InputHandler.key_released[key] = False
        for key in InputHandler.key_pressed.keys():
            InputHandler.key_pressed[key] = False

    @staticmethod
    def key_binding_pressed(name: str) -> bool:
        codes: list[int] = Config.Keybindings[name]
        return True in [InputHandler.key_pressed.get(code, "False") for code in codes]

    @staticmethod
    def key_binding_held(name: str) -> bool:
        codes: list[int] = Config.Keybindings[name]
        return True in [InputHandler.key_held.get(code, "False") for code in codes]

    @staticmethod
    def key_binding_released(name: str) -> bool:
        codes: list[int] = Config.Keybindings[name]
        return True in [InputHandler.key_released.get(code, "False") for code in codes]


if __name__ == '__main__':
    pass
