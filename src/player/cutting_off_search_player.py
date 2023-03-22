from typing import Tuple
from copy import deepcopy
from state import State
from .player import Player

inf = 10000

class CuttingOffSearchPlayer(Player):

    def __init__(self, max_depth, evaluation_func=None):
        """
        Player based on cutting off alpha-beta search.
        Parameters:
            max_depth: maximum searching depth. The search will stop when the depth exists max_depth.
            evaluation_func: a function taking a state as input and
                outputs the value in the current player's perspective.
        """
        super().__init__()
        self.max_depth = max_depth
        self.evaluation_func = (lambda s: 0) if evaluation_func is None else evaluation_func

    def evaluation(self, state: State):
        """
        Calculate the evaluation value relative to the agent player (rather than state's current player),
        i.e., take negation if the current player is opponent or do nothing else wise.
        """
        value = self.evaluation_func(state)
        if self.player != state.get_current_player():
            value = -value
        return value

    def get_action(self, state: State):
        """
        An interface for recursively searching.
        """
        assert state.get_current_player() == self.player

        def cutting_off_alpha_beta_search(s: State, d, alpha, beta):
            """
            Search for several depth and use evaluation value as cutting off.

            Parameters:
                s: the current state
                d: the remaining search depth, the search will stop when d=0
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
            elif d == 0:
                value = self.evaluation_func(s)
            else:
                # TODO
                flag =  self.player == s.get_current_player()
                value = -inf if flag else inf  # MAX node / MIN node
                state_copy = deepcopy(s)
                for act_temp in s.get_all_actions():
                    if flag:     # MAX node
                        state_copy.perform_action(act_temp) 
                        temp_value, _ = cutting_off_alpha_beta_search(state_copy, d, alpha, beta)
                        state_copy.cancel_action()
                        if temp_value > value:
                            value = temp_value
                            action = act_temp
                        if value >= beta:
                            return value, action
                        alpha = max(alpha, value)
                    else:        # MIN node
                        state_copy.perform_action(act_temp) 
                        temp_value, _ = cutting_off_alpha_beta_search(state_copy, d - 1, alpha, beta)
                        state_copy.cancel_action()
                        if temp_value < value: 
                            value = temp_value
                            # action = act_temp
                        if value <= alpha:
                            return value, action
                        beta = min(beta, value)

            return value, action

        return cutting_off_alpha_beta_search(state, self.max_depth, -inf, inf)[1]
