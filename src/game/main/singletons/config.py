import json
import arcade.key as arcade_keys

from src.game.main.singletons.singleton import Singleton
from src.game.main.util.path_loader import get_absolute_resource_path


class Config(metaclass=Singleton):

    Keybindings = {}
    Settings = {}
    Constants = {}

    @staticmethod
    def load():
        Config.load_settings()
        Config.load_keybindings()
        Config.load_constants()


    @staticmethod
    def load_keybindings() -> None:
        with open(get_absolute_resource_path("\\configs\\keybindings.json"), "r") as f:
            keybindings: dict = json.load(f)

        for name, value in keybindings.items():
            Config.Keybindings[name] = [getattr(arcade_keys, key) for key in value]


    @staticmethod
    def load_settings() -> None:
        with open(get_absolute_resource_path("\\configs\\settings.json"), "r") as f:
            settings: dict = json.load(f)

        for name, value in settings.items():
            Config.Settings[name] = value


    @staticmethod
    def load_constants() -> None:
        with open(get_absolute_resource_path("\\configs\\constants.json"), "r") as f:
            constants: dict = json.load(f)

        for name, value in constants.items():
            Config.Constants[name] = value


