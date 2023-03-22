from typing import List, Tuple

class State(object):
    """A general state for two-player zero-sum game."""

    def __init__(self):
        self._players = [1, 2]
        self._current_player = None

    def reset(self):
        raise NotImplementedError

    def get_current_player(self) -> int:
        raise NotImplementedError

    def get_all_actions(self) -> List:
        raise NotImplementedError
    
    def get_last_move(self) -> int:
        raise NotImplementedError

    def perform_action(self, action):
        raise NotImplementedError

    def game_end(self) -> Tuple[bool, int]:
        raise NotImplementedError

    def get_info(self):
        return None