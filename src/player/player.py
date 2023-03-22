from state import State

class Player(object):
    """A general player for two-player zero-sum game."""

    def __init__(self):
        self.player = None

    def set_player(self, p):
        self.player = p

    def get_action(self, state: State):
        raise NotImplementedError

    def __str__(self):
        return f"{self.__class__.__name__} {self.player}"