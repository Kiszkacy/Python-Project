from typing import List, Optional

import arcade

from src.game.main.entities.enemies.station.station import EnemyStation
from src.game.main.entities.entity import Entity
from src.game.main.entities.formations.trade_station import TradeStation
from src.game.main.entities.friendly.weapon_station import WeaponStation
from src.game.main.entities.player_ship import PlayerShip
from src.game.main.entities.friendly.portal import Portal
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.events.destroy_event import DestroyEvent
from src.game.main.events.event import Event
from src.game.main.events.event_observer import Observer
from src.game.main.events.spawn_event import SpawnEvent
from src.game.main.interfaces.processable import Processable
from src.game.main.singletons.config import Config
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.singletons.event_register import EventRegister
from src.game.main.util.math import normalize
from src.game.main.util.path_loader import get_absolute_resource_path


class HUDWaypoint(Observer, Processable):

    def __init__(self) -> None:
        self.player_ship: PlayerShip = EntityHandler.player
        self.circle_sprite: arcade.Sprite = arcade.Sprite(get_absolute_resource_path("\\sprites\\hud_waypoint_circle.png"), scale=0.5)
        self.waypoints_markers: List[arcade.Sprite] = []
        self.waypoints: List[Entity] = []

    def init(self) -> None:
        EventRegister.add_observer(self)
        # circle sprite
        self.circle_sprite.position = (Config.Settings.get("SCREEN_WIDTH") / 2.0, Config.Settings.get("SCREEN_HEIGHT") / 2.0)
        EntityHandler.add(self.circle_sprite, ObjectCategory.HUD)

        # check if interesting objects are already placed in the sector
        enemy_station_idx: Optional[int] = None
        for idx, e in enumerate(EntityHandler.categorized[ObjectCategory.ENEMIES]):
            if isinstance(e, EnemyStation):
                enemy_station_idx = idx
                break
        if enemy_station_idx is not None:
            self.waypoints.append(EntityHandler.categorized[ObjectCategory.ENEMIES][enemy_station_idx])
            self.waypoints_markers.append(arcade.Sprite(texture=arcade.make_circle_texture(32, (230, 123, 100, 32))))
            EntityHandler.add(self.waypoints_markers[-1], ObjectCategory.HUD)

        # friendly station
        friendly_station_idx: Optional[int] = None
        for idx, e in enumerate(EntityHandler.categorized[ObjectCategory.FRIENDLY]):
            if isinstance(e, WeaponStation):
                friendly_station_idx = idx
                break
        if friendly_station_idx is not None:
            self.waypoints.append(EntityHandler.categorized[ObjectCategory.FRIENDLY][friendly_station_idx])
            self.waypoints_markers.append(arcade.Sprite(texture=arcade.make_circle_texture(32, (100, 230, 230, 32))))
            EntityHandler.add(self.waypoints_markers[-1], ObjectCategory.HUD)

        print("MARKERS", self.waypoints_markers)
        print("MARKERS", self.waypoints)

    def notify(self, event: Event) -> None:
        if isinstance(event, SpawnEvent) and isinstance(event.spawned, Portal):
            self.waypoints.append(event.spawned)
            self.waypoints_markers.append(arcade.Sprite(texture=arcade.make_circle_texture(32, (93, 218, 95, 32))))
            EntityHandler.add(self.waypoints_markers[-1], ObjectCategory.HUD)
        elif isinstance(event, DestroyEvent) and isinstance(event.destroyed, EnemyStation) and event.destroyed in self.waypoints:
            idx: int = self.waypoints.index(event.destroyed)
            self.waypoints.pop(idx)
            self.waypoints_markers[idx].kill()
            self.waypoints_markers.pop(idx)

    def process(self, delta: float) -> None:
        # calculate angle from player to each waypoint and draw on screen
        for marker, waypoint in zip(self.waypoints_markers, self.waypoints):
            x_diff: float = waypoint.position[0] - self.player_ship.position[0]
            y_diff: float = waypoint.position[1] - self.player_ship.position[1]
            # target_angle_rad: float = np.arctan2(y_diff, x_diff)
            # if target_angle_rad < 0:
            #     target_angle_rad += 2 * math.pi
            circle_radius: float = 235.0
            # rotated: List[float] = arcade.rotate_point(circle_radius + self.station.position[0],
            #                                            0 + self.station.position[1],
            #                                            self.station.position[0], self.station.position[1],
            #                                            self.orbit_angle)
            dir: arcade.Point = normalize((x_diff, y_diff))
            offset: arcade.Point = (dir[0] * circle_radius, dir[1] * circle_radius)
            marker.position = (Config.Settings.get("SCREEN_WIDTH") / 2.0 + offset[0], Config.Settings.get("SCREEN_HEIGHT") / 2.0 + offset[1])


if __name__ == '__main__':
    pass
