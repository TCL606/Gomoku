from .player import Player
from state import Board

class Human(Player):

    def get_action(self, state: Board):
        try:
            location = input("Your move: ")
            if isinstance(location, str):  # for python3
                location = [int(n, 10) for n in location.split(",")]
            move = state.location_to_move(location)
        except Exception as e:
            move = -1
        if move == -1 or move not in state.get_all_actions():
            print("invalid move")
            move = self.get_action(state)
        return move