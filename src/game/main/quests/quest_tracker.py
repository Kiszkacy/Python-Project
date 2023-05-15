from src.game.main.entities.enemies.enemy import Enemy
from src.game.main.events.destroy_event import DestroyEvent
from src.game.main.events.event import Event
from src.game.main.events.event_observer import Observer
from src.game.main.events.pickup_event import PickupEvent
from src.game.main.quests.quest import Quest
from src.game.main.quests.quest_gather_ore import QuestGatherOre
from src.game.main.quests.quest_type import QuestType
from src.game.main.singletons.event_register import EventRegister


class QuestTracker(Observer):

    def __init__(self, quest: Quest) -> None:
        self.quest: Quest = quest

    def setup(self) -> None:
        EventRegister.add_observer(self)

    def notify(self, event: Event) -> None:
        if self.check_if_valid(event):
            self.quest.advance(1)

    def check_if_valid(self, event: Event) -> bool:
        if self.quest.type_ == QuestType.KILL_SUM and isinstance(event, DestroyEvent):
            destroy_event: DestroyEvent = event
            return isinstance(destroy_event.destroyed, Enemy)

        if self.quest.type_ == QuestType.GATHER_ORE and isinstance(event, PickupEvent):
            quest_: QuestGatherOre = self.quest
            pickup_event: PickupEvent = event
            return quest_.ore_type == pickup_event.picked

    def is_completed(self) -> bool:
        return self.quest.is_completed()


if __name__ == '__main__':
    pass
