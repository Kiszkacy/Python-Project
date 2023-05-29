from src.game.main.singletons.game_save import GameSave
from src.game.main.singletons.player_statistics import PlayerStatistics


def on_exit():
    PlayerStatistics.save()
    GameSave.save()
