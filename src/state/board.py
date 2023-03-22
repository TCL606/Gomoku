import numpy as np
from .state import State

class Board(State):
    """board for the game"""

    def __init__(self, **kwargs):
        super().__init__()
        self.width = int(kwargs.get('width', 8))
        self.height = int(kwargs.get('height', 8))
        # board states stored as a dict,
        # key: move as location on the board,
        # value: player as pieces type
        self._states = {}
        # need how many pieces in a row to win
        self._n_in_row = int(kwargs.get('n_in_row', 5))
        self._availables, self._last_move = None, None

    def move_to_location(self, move):
        h = move // self.width
        w = move % self.width
        return [h, w]

    def location_to_move(self, location):
        if len(location) != 2:
            return -1
        h = location[0]
        w = location[1]
        move = h * self.width + w
        if move not in range(self.width * self.height):
            return -1
        return move

    def reset(self, start_player=0):
        if self.width < self._n_in_row or self.height < self._n_in_row:
            raise Exception('board width and height can not be '
                            'less than {}'.format(self._n_in_row))
        self._current_player = self._players[start_player]  # start player
        # keep available moves in a list
        self._availables = list(range(self.width * self.height))
        self._states = {}
        self._last_move = -1
        self.can_cancel = False

    def get_current_player(self):
        return self._current_player
    
    def get_last_move(self):
        return self._last_move

    def get_all_actions(self):
        return self._availables

    def perform_action(self, action):
        self._states[action] = self._current_player
        self._availables.remove(action)
        self._current_player = (
            self._players[0] if self._current_player == self._players[1]
            else self._players[1]
        )
        self._last_move = action
        self.can_cancel = True
        return self

    def cancel_action(self):
        if self.can_cancel:
            self._current_player = (
                self._players[0] if self._current_player == self._players[1]
                else self._players[1]
            )
            self._availables.append(self._last_move)
            del self._states[self._last_move]
            self.can_cancel = False
        return self

    def has_a_winner(self):
        width = self.width
        height = self.height
        states = self._states
        n = self._n_in_row

        moved = list(set(range(width * height)) - set(self._availables))
        if len(moved) < self._n_in_row * 2 - 1:
            return False, -1

        for m in moved:
            h = m // width
            w = m % width
            player = states[m]

            if (w in range(width - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n))) == 1):
                return True, player

            if (h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * width, width))) == 1):
                return True, player

            if (w in range(width - n + 1) and h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * (width + 1), width + 1))) == 1):
                return True, player

            if (w in range(n - 1, width) and h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * (width - 1), width - 1))) == 1):
                return True, player

        return False, -1

    def game_end(self):
        """Check whether the game is ended or not"""
        win, winner = self.has_a_winner()
        if win:
            return True, winner
        elif not len(self._availables):
            return True, -1
        return False, -1

    def get_info(self):
        info_dict = {
            "live_four": [
                np.array([0, 1, 1, 1, 1, 0]),
            ],
            "four": [
                np.array([0, 1, 1, 1, 1]),
                np.array([0, 1, 1, 1, 0, 1]),
                np.array([0, 1, 1, 0, 1, 1]),
                np.array([0, 1, 0, 1, 1, 1]),
                np.array([1, 1, 1, 1, 0]),
                np.array([1, 0, 1, 1, 1, 0]),
                np.array([1, 1, 0, 1, 1, 0]),
                np.array([1, 1, 1, 0, 1, 0]),
            ],
            "live_three": [
                np.array([0, 1, 1, 1, 0]),
                np.array([0, 1, 1, 0, 1, 0]),
                np.array([0, 1, 0, 1, 1, 0]),
            ],
            "three": [
                np.array([0, 1, 1, 1]),
                np.array([0, 1, 1, 0, 1]),
                np.array([0, 1, 0, 1, 1]),
                np.array([1, 1, 1, 0]),
                np.array([1, 1, 0, 1, 0]),
                np.array([1, 0, 1, 1, 0]),
            ],
            "live_two": [
                np.array([0, 1, 1, 0]),
                np.array([0, 1, 0, 1, 0]),
            ],
        }

        state = np.zeros((self.width, self.height))
        if len(self._states) > 0:
            moves, players = np.array(list(zip(*self._states.items())))
            state[moves // self.width, moves % self.height] = players

        all_state = -np.ones((4, 6, self.width, self.height))
        all_state[0, 0] = state
        all_state[1, 0] = state
        all_state[2, 0] = state
        all_state[3, 0] = state
        for i in range(1, 6):
            all_state[0, i, :-i, :] = state[i:, :]
            all_state[1, i, :, :-i] = state[:, i:]
            all_state[2, i, :-i, :-i] = state[i:, i:]
            all_state[3, i, :-i, i:] = state[i:, :-i]

        info = {}

        for player in self._players:
            info[player] = {}
            occupied = np.zeros((4, 6, self.width, self.height), dtype=bool)
            for shape_name, shape_list in info_dict.items():
                info[player][shape_name] = 0
                for shape in shape_list:
                    match = np.all((~occupied[:, :len(shape), :, :]) & (all_state[:, :len(shape), :, :] == player * shape[None, :, None, None]), axis=1)
                    info[player][shape_name] += match.sum()
                    for d, w_0, h_0 in np.transpose(match.nonzero()):
                        for j in range(len(shape)):
                            if d == 0:
                                w, h = w_0 + j, h_0
                            elif d == 1:
                                w, h = w_0, h_0 + j
                            elif d == 2:
                                w, h = w_0 + j, h_0 + j
                            else:
                                w, h = w_0 + j, h_0 - j
                            for i in range(6):
                                if d == 0 and w >= i:
                                    occupied[0, i, w - i, h] = 1
                                if d == 1 and h >= i:
                                    occupied[1, i, w, h - i] = 1
                                if d == 2 and w >= i and h >= i:
                                    occupied[2, i, w - i, h - i] = 1
                                if d == 3 and w >= i and h + i < self.height:
                                    occupied[3, i, w - i, h + i] = 1
            max_distance = max([0.] + [abs(location // self.width - (self.height - 1) / 2)
                                       + abs(location % self.width - (self.width - 1) / 2)
                                       for location in self._states.keys() if
                                       self._states.get(location, 0) == player])
            max_distance /= ((self.height - 1) / 2 + (self.width - 1) / 2)
            info[player]["max_distance"] = max_distance

        return info

