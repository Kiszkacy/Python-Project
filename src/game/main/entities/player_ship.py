
import arcade
import numpy as np

from src.game.main.entities.ship import Ship
from src.game.main.enums.input_mode import InputMode
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.singletons.config import Config
from src.game.main.singletons.input_handler import InputHandler
from src.game.main.util.math import map_range, clamp
from src.game.main.util.path_loader import get_absolute_resource_path
from src.game.main.weapons.aura.aura import WeaponAura
from src.game.main.weapons.basic.basic import WeaponBasic
from src.game.main.weapons.shotgun.shotgun import WeaponShotgun
from src.game.main.weapons.sinus.sinus import WeaponSinus
from src.game.main.weapons.weird.weird import WeaponWeird


class PlayerShip(Ship):

    def __init__(self, starting_position: arcade.Point) -> None:
        super().__init__(sprite_url=get_absolute_resource_path("\\sprites\\tmp_ship0.png"),
                         mass=50.0,
                         weapons=[WeaponBasic(), WeaponShotgun(), WeaponAura(), WeaponSinus(), WeaponWeird()],
                         weapon_count=5,
                         belongs_to=ObjectCategory.PLAYER,
                         collides_with=[ObjectCategory.STATIC, ObjectCategory.ENEMIES, ObjectCategory.PROJECTILES, ObjectCategory.MISC])
        self.position = starting_position
        self.dashes_max: int = Config.Constants.get("DASHES_MAX")
        self.dashes: int = self.dashes_max
        # SCRIPT VARS "PRIVATE"
        self.dash_timer: float = 0.0
        self.dash_timer_online: bool = False

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.process_input(delta_time)
        self.rotate_towards_mouse(delta_time)
        super(PlayerShip, self).on_update()
        # update dash timer
        if self.dash_timer_online:
            self.dash_timer -= delta_time
            if self.dash_timer <= 0.0:
                self.dash_regen()

    def process_input(self, delta: float) -> None:
        if InputHandler.mode is not InputMode.INGAME: return

        if InputHandler.key_binding_held("SHOOT"): # TODO switch to mouse
            self.fire()
        if InputHandler.key_binding_held("ALTFIRE"): # TODO switch to mouse
            self.altfire()
        if InputHandler.key_binding_held("FLY"):
            self.fly(delta)
        if InputHandler.key_binding_pressed("WEAPON0"):
            self.switch_weapon(0)
        if InputHandler.key_binding_pressed("WEAPON1"):
            self.switch_weapon(1)
        if InputHandler.key_binding_pressed("WEAPON2"):
            self.switch_weapon(2)
        if InputHandler.key_binding_pressed("WEAPON3"):
            self.switch_weapon(3)
        if InputHandler.key_binding_pressed("WEAPON4"):
            self.switch_weapon(4)
        if InputHandler.key_binding_pressed("DASH_TRIGGER"):
            if InputHandler.key_binding_held("DASH_LEFT"):
                self.dash(left=True)
            elif InputHandler.key_binding_held("DASH_RIGHT"):
                self.dash(left=False)

    def fly(self, delta: float) -> None:
        direction: arcade.Vector = (np.cos(np.deg2rad(self.angle)), np.sin(np.deg2rad(self.angle))) # already normalized
        velocity_direction: arcade.Vector = (np.cos(np.deg2rad(self.velocity[0])), np.sin(np.deg2rad(self.velocity[1]))) # already normalized
        x_diff: float = direction[0] - velocity_direction[0]
        y_diff: float = direction[1] - velocity_direction[1]
        angle_rad: float = np.arctan2(y_diff, x_diff)
        strength: float = map_range(abs(angle_rad), 0.0, np.pi, 1.0, 2.0)
        acceleration_vector: arcade.Vector = (direction[0]*self.acceleration, direction[1]*self.acceleration)
        self.velocity = (self.velocity[0] + acceleration_vector[0]*strength*delta, self.velocity[1] + acceleration_vector[1]*strength*delta)
        self.velocity = clamp(self.velocity, 0.0, self.max_speed)

    def rotate_towards_mouse(self, delta: float) -> None:
        mouse: arcade.Point = InputHandler.mouse

        x_diff: float = mouse[0] - Config.Settings.get("SCREEN_WIDTH") / 2.0 # TODO may create weird behavior when player is moving at high speeds
        y_diff: float = mouse[1] - Config.Settings.get("SCREEN_HEIGHT") / 2.0
        target_angle_rad: float = np.arctan2(y_diff, x_diff)
        self.rotate_towards(delta, target_angle_rad)

    def dash(self, left: bool) -> None:
        if self.dashes <= 0: return
        # TODO get rid of constants !!!
        direction: arcade.Vector = (np.cos(np.deg2rad(self.angle)), np.sin(np.deg2rad(self.angle))) # already normalized
        dash_force: arcade.Vector
        if left:    dash_force = (-direction[1] * self.max_speed, direction[0] * self.max_speed)
        else:       dash_force = (direction[1] * self.max_speed, -direction[0] * self.max_speed)
        self.velocity = dash_force

        self.dashes -= 1
        self.dash_regen_request()

    def dash_regen_request(self) -> None:
        if self.dash_timer_online: return
        self.dash_timer_online = True
        self.dash_timer = Config.Constants.get("DASH_CD")

    def dash_regen(self) -> None:
        self.dashes += 1
        if self.dashes == self.dashes_max: # stop when at max dashes
            self.dash_timer_online = False
            return
        self.dash_timer = Config.Constants.get("DASH_CD")



if __name__ == '__main__':
    pass
