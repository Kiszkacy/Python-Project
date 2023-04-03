import json
import arcade.key as arcade_keys
from src.singletons.Singleton import Singleton


class Config(metaclass=Singleton):

    Keybindings = {}

    @staticmethod
    def load_config():
        with open("..\\resources\\configs\\KeyBindings.json", "r") as f:
            configs : dict = json.load(f)

        for name, value in configs.items():
            Config.Keybindings[name] = [getattr(arcade_keys, key) for key in value]
