from state import State
from player import Player

class Game(object):
    def __init__(self, board: State, **kwargs):
        self.player = None
        self.board = board

    def graphic(self, board: State, player1, player2):
        raise NotImplementedError

    def start_play(self, player1: Player, player2: Player, start_player=0, is_shown=1):
        raise NotImplementedError
    
    
    