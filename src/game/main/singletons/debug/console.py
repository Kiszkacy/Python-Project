
import arcade
import arcade.gui
import numpy as np
from arcade import load_texture
from arcade.gui import UIManager, UITexturePane, UIInputText, UIBoxLayout, UITextArea

from src.game.main.entities.asteroids.asteroidMedium import AsteroidMedium
from src.game.main.entities.asteroids.asteroidSmall import AsteroidSmall
from src.game.main.entities.player_ship import PlayerShip
from src.game.main.enums.input_mode import InputMode
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.singletons.config import Config
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.singletons.input_handler import InputHandler
from src.game.main.singletons.singleton import Singleton
from src.game.main.util.math import magnitude
from src.game.main.util.path_loader import get_absolute_resource_path


class Console(metaclass=Singleton):

    # console box
    draw_console_box: bool = False
    manager: arcade.gui.UIManager = None
    # memory
    last_command: str = ""
    last_args: list[str] = []

    @staticmethod
    def init() -> None:
        Console.manager = UIManager()
        Console.manager.enable()
        bg_tex: arcade.Texture = load_texture(get_absolute_resource_path("\\sprites\\console_bg.png"))
        Console.manager.add(
            UITexturePane(
                UIBoxLayout(
                    x=Config.Settings.get("SCREEN_WIDTH") // 2 - 256,
                    y=Config.Settings.get("SCREEN_HEIGHT") - 64,
                    children=(
                        UITextArea(
                                    x=0,
                                    y=0,
                                    width=512,
                                    height=512-32,
                                    text="",
                                    font_size=14,
                                    text_color=(255,255,255,255)).with_space_around(),
                        UIInputText(
                                    x=0,
                                    y=0,
                                    width=512, height=32, text="",
                                    multiline=False,
                                    font_size=14,
                                    active=False,
                                    text_color=(255,255,255,255))
                    )
                ),
                tex=bg_tex,
                padding=(16, 16, 16, 16),
            )
        )


    @staticmethod
    def on_update() -> None:
        # make input automatically active/inactive if opened/closed
        if InputHandler.mode is not InputMode.CONSOLE:
            input_box: UIInputText = Console.manager.children[0][0].children[0].children[1] # TODO ???????
            input_box._active = False
        else:
            input_box: UIInputText = Console.manager.children[0][0].children[0].children[1] # TODO ???????
            input_box._active = True
        # check console text
        input_box: UIInputText = Console.manager.children[0][0].children[0].children[1] # TODO ???????
        output_box: UITextArea = Console.manager.children[0][0].children[0].children[0].children[0] # TODO ???????
        if len(input_box.text) == 0: return
        if input_box.text[-1] == '\n':
            output_box.text += input_box.text
            text: str = input_box.text[:-1]
            if text.split() != []:
                command: str = text.split()[0]
                args: list[str] = text.split()[1:]
                Console.run_command(command, args, len(args))
            input_box.text = ""


    @staticmethod
    def draw() -> None:
        if Console.draw_console_box:
            Console.manager.draw()


    @staticmethod
    def run_command(command: str, args: list[str], argc: int) -> None:
        # save this command
        if command not in ["r", "repeat"]: # inf recursion safeguard
            Console.last_command = command
            Console.last_args = args
        match command:
            case "d" | "damage":
                player: PlayerShip = EntityHandler.categorized[ObjectCategory.PLAYER][0] # TODO ugly
                if player is None: return
                player.damage(float(args[0]))
            case "s" | "spawn":
                match args[0]:
                    case "a" | "asteroid":
                        if argc <= 1: Console.spawn_small_asteroid((0,0)); return
                        match args[1]:
                            case "s" | "small":
                                if argc == 2:   Console.spawn_small_asteroid((0,0))
                                else:           Console.spawn_small_asteroid((float(args[2]), float(args[3])))
                            case "m" | "medium":
                                if argc == 2:   Console.spawn_medium_asteroid((0, 0))
                                else:           Console.spawn_medium_asteroid((float(args[2]), float(args[3])))
            case "r" | "repeat":
                Console.run_command(Console.last_command, Console.last_args, len(Console.last_args))
            case _:
                pass

    @staticmethod
    def spawn_small_asteroid(offset: arcade.Vector) -> None:
        player: PlayerShip = EntityHandler.categorized[ObjectCategory.PLAYER][0] # TODO ugly
        if player is None: return
        EntityHandler.add(
            AsteroidSmall(
                starting_position=(player.position[0] + offset[0], player.position[1] + offset[1]),
                starting_velocity=(np.random.randint(-50, 50), np.random.randint(-50, 50))
            ),
            ObjectCategory.MISC
        )

    @staticmethod
    def spawn_medium_asteroid(offset: arcade.Vector) -> None:
        player: PlayerShip = EntityHandler.categorized[ObjectCategory.PLAYER][0] # TODO ugly
        if player is None: return
        EntityHandler.add(
            AsteroidMedium(
                starting_position=(player.position[0] + offset[0], player.position[1] + offset[1]),
                starting_velocity=(np.random.randint(-50, 50), np.random.randint(-50, 50))
            ),
            ObjectCategory.MISC
        )


if __name__ == '__main__':
    pass
