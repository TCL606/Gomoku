from typing import Tuple
from copy import deepcopy
from state import State
from .player import Player

inf = 10000

class MinimaxSearchPlayer(Player):
    """
    Player based on minimax search.
    """

    def get_action(self, state: State):
        """
        An interface for recursively searching.
        """
        assert state.get_current_player() == self.player

        def minimax_search(s: State) -> Tuple:
            """
            Recursively search values of all succeeding nodes, taking maximum of children
            when current player is the agent (self.player) and minimum for opponent.

            Parameters:
                s: the current state

            Return:
                Tuple(value, action): the node value and the best action (if exists)
            
            Note: before you perform an action, you might need to copy the original state for in-place update.
            """
            end, winner = s.game_end()
            value, action = None, None
            if end:
                if winner == -1:
                    value = 0
                else:
                    value = (1 if winner == self.player else -1)
            else:
                # TODO
                flag = self.player == s.get_current_player()
                value = -inf if flag else inf  # MAX node / MIN node
                state_copy = deepcopy(s)
                for act_temp in s.get_all_actions():
                    if flag:     # MAX node
                        state_copy.perform_action(act_temp) 
                        temp_value, _ = minimax_search(state_copy)
                        state_copy.cancel_action()
                        if temp_value > value:
                            value = temp_value
                            action = act_temp
                    else:        # MIN node
                        state_copy.perform_action(act_temp) 
                        temp_value, _ = minimax_search(state_copy)
                        state_copy.cancel_action()
                        if temp_value < value: 
                            value = temp_value
                            # action = act_temp
            return value, action

        return minimax_search(state)[1]
