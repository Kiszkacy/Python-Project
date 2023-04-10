
import arcade
import arcade.gui
import numpy as np
from arcade import load_texture
from arcade.gui import UIManager, UITexturePane, UIInputText, UIBoxLayout, UITextArea

from src.auxilary.InputMode import InputMode
from src.auxilary.ObjectCategory import ObjectCategory
from src.entities.PlayerShip import PlayerShip
from src.entities.asteroids.asteroidSmall import AsteroidSmall
from src.singletons.Config import Config
from src.singletons.EntityHandler import EntityHandler
from src.singletons.InputHandler import InputHandler
from src.singletons.Singleton import Singleton
from src.util.VectorMath import length


class DebugConsole(metaclass=Singleton):

    critical_text_font_size: int = 20
    critical_text_screen_offset: int = 15
    critical_text_line_offset: int = 30
    critical_text_line_count: int = 10
    draw_critical: bool = False
    draw_console_box: bool = False
    critical_text: list[arcade.Text] = []
    manager: arcade.gui.UIManager = None
    last_command: str = ""
    last_args: list[str] = []


    @staticmethod
    def init() -> None:
        DebugConsole.critical_text = [arcade.Text(f"DEBUG CRITICAL TEXT LINE {i}",
                                                  start_x=DebugConsole.critical_text_screen_offset,
                                                  start_y=DebugConsole.critical_text_screen_offset + DebugConsole.critical_text_line_offset * i,
                                                  color=arcade.color.WHITE,
                                                  font_size=DebugConsole.critical_text_font_size)
                                      for i in range(DebugConsole.critical_text_line_count)]
        DebugConsole.manager = UIManager()
        DebugConsole.manager.enable()
        bg_tex: arcade.Texture = load_texture("..\\resources\\sprites\\console_bg.png")
        DebugConsole.manager.add(
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
    def on_update(camera: arcade.Camera) -> None:
        # make input automatically active/inactive if opened/closed
        if InputHandler.mode is not InputMode.CONSOLE:
            input_box: UIInputText = DebugConsole.manager.children[0][0].children[0].children[1]  # TODO ???????
            input_box._active = False
        else:
            input_box: UIInputText = DebugConsole.manager.children[0][0].children[0].children[1]  # TODO ???????
            input_box._active = True
        # update critical text
        player: PlayerShip = EntityHandler.categorized[ObjectCategory.PLAYER][0] # TODO ugly
        if player is not None:
            texts: list[str] = [f"FPS: {arcade.get_fps()}",
                                f"Cursor: {InputHandler.mouse[0]} {InputHandler.mouse[1]}",
                                f"Player: {player.position}",
                                f"Camera: {camera.position[0] + Config.Settings.get('SCREEN_WIDTH') / 2.0, camera.position[1] + Config.Settings.get('SCREEN_HEIGHT') / 2.0}",
                                f"Active weapon idx: {player.weapon_idx}",
                                f"Space: {InputHandler.key_pressed.get(arcade.key.SPACE, False)}",
                                f"Player angle: {player.angle}",
                                f"Player power: {player.power}",
                                f"Player velocity: {player.velocity}",
                                f"Player speed: {length(player.velocity)}"]
            for idx, line in enumerate(DebugConsole.critical_text):
                line.text = texts[idx]
        # check console text
        input_box: UIInputText = DebugConsole.manager.children[0][0].children[0].children[1] # TODO ???????
        output_box: UITextArea = DebugConsole.manager.children[0][0].children[0].children[0].children[0] # TODO ???????
        if len(input_box.text) == 0: return
        if input_box.text[-1] == '\n':
            output_box.text += input_box.text
            text: str = input_box.text[:-1]
            if text.split() != []:
                command: str = text.split()[0]
                DebugConsole.run_command(command, text.split()[1:])
            input_box.text = ""


    @staticmethod
    def draw() -> None:
        if DebugConsole.draw_critical:
            for text in DebugConsole.critical_text:
                text.draw()
        # ui class draw
        if DebugConsole.draw_console_box:
            DebugConsole.manager.draw()


    @staticmethod
    def run_command(command: str, args: list[str]) -> None:
        # save this command
        if command not in ["r", "repeat"]: # inf recursion
            DebugConsole.last_command = command
            DebugConsole.last_args = args
        match command:
            case "d" | "damage":
                player: PlayerShip = EntityHandler.categorized[ObjectCategory.PLAYER][0]  # TODO ugly
                if player is None: return
                player.damage(float(args[0]))
            case "s" | "spawn":
                player: PlayerShip = EntityHandler.categorized[ObjectCategory.PLAYER][0]  # TODO ugly
                if player is None: return
                match args[0]:
                    case "a" | "asteroid":
                        EntityHandler.add(
                            AsteroidSmall(
                                starting_position=(player.position[0] + 256, player.position[1]),
                                starting_velocity=(np.random.randint(-50, 50), np.random.randint(-50, 50))
                            ),
                            ObjectCategory.MISC
                        )
            case "r" | "repeat":
                DebugConsole.run_command(DebugConsole.last_command, DebugConsole.last_args)
            case _:
                pass




if __name__ == '__main__':
    pass
