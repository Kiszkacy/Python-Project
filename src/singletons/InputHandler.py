
import arcade
from src.singletons.Singleton import Singleton


class InputHandler(metaclass=Singleton):

    mouse: arcade.Point = (0,0)
    key_pressed: list[bool] = [False for _ in range(65535)] # TODO fix me later please ;-;
    key_released: list[bool] = [False for _ in range(65535)] # TODO fix me later please ;-;

    @staticmethod
    def clean() -> None:
        InputHandler.key_released = [False for i in range(65535)]


if __name__ == '__main__':
    pass
