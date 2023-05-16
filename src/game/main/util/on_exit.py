from src.game.main.singletons.player_statistics import PlayerStatistics


def on_exit():
    PlayerStatistics.save()