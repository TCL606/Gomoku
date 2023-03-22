from typing import Tuple
from copy import deepcopy
from state import State
from .player import Player

inf = 10000
class AlphaBetaSearchPlayer(Player):
    """
    Player based on alpha-beta search.
    """

    def get_action(self, state: State):
        """
        An interface for recursively searching.
        """
        assert state.get_current_player() == self.player

        def alpha_beta_search(s: State, alpha, beta):
            """
            Based on minimax search, record current maximum value of the max player (alpha)
            and current minimum value of the min player (beta), use alpha and beta to prune.

            Parameters:
                s: the current state
                alpha: the current maximum value of the max player
                beta: the current minimum value of the min player

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
                flag =  self.player == s.get_current_player()
                value = -inf if flag else inf  # MAX node / MIN node
                for act_temp in s.get_all_actions():
                    state_copy = deepcopy(s)
                    if flag:     # MAX node
                        state_copy.perform_action(act_temp) 
                        temp_value, _ = alpha_beta_search(state_copy, alpha, beta)
                        if temp_value > value:
                            value = temp_value
                            action = act_temp
                        if value >= beta:
                            return value, action
                        alpha = max(alpha, value)
                    else:        # MIN node
                        state_copy.perform_action(act_temp) 
                        temp_value, _ = alpha_beta_search(state_copy, alpha, beta)
                        if temp_value < value: 
                            value = temp_value
                            # action = act_temp
                        if value <= alpha:
                            return value, action
                        beta = min(beta, value)

            return value, action

        return alpha_beta_search(state, -inf, inf)[1]
