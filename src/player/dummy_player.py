from .player import Player

class DummyPlayer(Player):
    def get_action(self, state):
        return state.get_all_actions()[0]
