import json
import random
import time

from src.game.main.entities.enemies.enemy import Enemy
from src.game.main.entities.player_ship import PlayerShip
from src.game.main.events.destroy_event import DestroyEvent
from src.game.main.events.event_observer import Observer
from src.game.main.quests.quest import Quest
from src.game.main.singletons.event_register import EventRegister
from src.game.main.singletons.singleton import Singleton
from src.game.main.events.event import Event
from src.game.main.util.path_loader import get_absolute_resource_path


class GameSave(Observer):

    stats: dict = {}
    player_alive = True


    @staticmethod
    def innit():
        try:
            with open(get_absolute_resource_path("\\configs\\save.json"), "r") as f:
                GameSave.stats = json.load(f)
        except IOError:
            GameSave.stats = {"seed": round(random.random() * time.time()), "exp": 0, "finished_sectors": []}
        finally:
            EventRegister.add_observer(GameSave())

    @staticmethod
    def save():
        with open(get_absolute_resource_path("\\configs\\save.json"), "w") as f:
            json.dump(GameSave.stats, f)

    def notify(self, event: Event) -> None:
        match event:
            case DestroyEvent(destroyed=Enemy()):
                self.stats["exp"] += 1

            case Quest():
                self.stats["exp"] += 10

            case DestroyEvent(destroyed=PlayerShip()):
                GameSave.player_alive = False
                #TODO save here maybe?
