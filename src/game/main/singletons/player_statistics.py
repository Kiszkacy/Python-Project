import json

from src.game.main.entities.enemies.enemy import Enemy
from src.game.main.entities.player_ship import PlayerShip
from src.game.main.events.destroy_event import DestroyEvent
from src.game.main.events.event_observer import Observer
from src.game.main.quests.quest import Quest
from src.game.main.singletons.event_register import EventRegister
from src.game.main.singletons.singleton import Singleton
from src.game.main.events.event import Event
from src.game.main.util.path_loader import get_absolute_resource_path


class PlayerStatistics(Observer):

    stats: dict = {}
    player_alive = True

    @staticmethod
    def init():
        try:
            with open(get_absolute_resource_path("\\configs\\players_statistics.json"), "r") as f:
                PlayerStatistics.stats = json.load(f)
                PlayerStatistics.stats["kills_this_round"] = 0
        except IOError:
            PlayerStatistics.stats = {"kills":0, "exp":0, "kills_this_round":0, "quests_completed":0}
        finally:
            EventRegister.add_observer(PlayerStatistics())

    @staticmethod
    def save():
        with open(get_absolute_resource_path("\\configs\\players_statistics.json"), "w") as f:
            json.dump(PlayerStatistics.stats, f)

    def notify(self, event: Event) -> None:
        match event:
            case DestroyEvent(destroyed=Enemy()):
                self.stats["kills"] += 1
                self.stats["kills_this_round"] += 1
                self.stats["exp"] += 1

            case Quest():
                self.stats["exp"] += 10
                self.stats["quests_completed"] += 1

            case DestroyEvent(destroyed=PlayerShip()):
                PlayerStatistics.player_alive = False
                #TODO save here maybe?
