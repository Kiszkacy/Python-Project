import json
import random
import time
from typing import Dict

from src.game.main.entities.enemies.enemy import Enemy
from src.game.main.entities.player_ship import PlayerShip
from src.game.main.events.destroy_event import DestroyEvent
from src.game.main.events.event_observer import Observer
from src.game.main.quests.quest import Quest
from src.game.main.singletons.event_register import EventRegister
from src.game.main.events.event import Event
from src.game.main.util.path_loader import get_absolute_resource_path


class GameSave(Observer):

    stats: Dict = None
    player_alive: bool = True

    @staticmethod
    def init() -> None:
        if GameSave.stats is None:
            try:
                with open(get_absolute_resource_path("\\saves\\save.json"), "r") as f:
                    GameSave.stats = json.load(f)
            except IOError:
                GameSave.stats = {"seed": round(random.random() * time.time()), "exp": 0, "finished_sectors": []}
            finally:
                EventRegister.add_observer(GameSave())

    @staticmethod
    def save() -> None:
        with open(get_absolute_resource_path("\\saves\\save.json"), "w") as f:
            json.dump(GameSave.stats, f)

    def notify(self, event: Event) -> None:
        match event:
            case DestroyEvent(destroyed=Enemy()):
                GameSave.stats["exp"] += 1

            case Quest():
                GameSave.stats["exp"] += 25

            case DestroyEvent(destroyed=PlayerShip()):
                GameSave.player_alive = False
                GameSave.save()
