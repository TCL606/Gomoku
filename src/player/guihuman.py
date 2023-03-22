from .player import Player
import threading
from state import Board

class GUIHuman(Player):

    def __init__(self, root, cell_size=30, R=10, C=10, board_shift_x=0.5, board_shift_y=0.5):
        super().__init__()
        self.root = root
        self.cell_size = cell_size
        self.R = R
        self.C = C
        self.board_shift_x = board_shift_x
        self.board_shift_y = board_shift_y
        self.event_sema = threading.BoundedSemaphore(1)
        self.event_sema.acquire()

    def process_event(self, event):
        self.event = event
        self.event_sema.release()

    def get_action(self, state: Board):
        try:
            self.root.bind("<ButtonPress-1>", self.process_event)
            self.event_sema.acquire()
            x = self.event.x - self.board_shift_x * self.cell_size
            y = self.event.y - self.board_shift_y * self.cell_size
            if x < 0:
                x = 0
            if x > (self.R - 1) * self.cell_size:
                x = (self.R - 1) * self.cell_size
            if y < 0:
                y = 0
            if y > (self.C - 1) * self.cell_size:
                y = (self.C - 1) * self.cell_size
            xa = int(x / self.cell_size)
            xb = x % self.cell_size
            ya = int(y / self.cell_size)
            yb = y % self.cell_size
            if xb >= self.cell_size / 2:
                cor_x = xa + 1
            else:
                cor_x = xa
            if yb >= self.cell_size / 2:
                cor_y = ya + 1
            else:
                cor_y = ya
            move = state.location_to_move([cor_x, cor_y])
            
        except Exception as e:
            move = -1

        finally:
            self.root.unbind("<ButtonPress-1>")

        if move == -1 or move not in state.get_all_actions():
            print("invalid move: ", move)
            move = self.get_action(state)
        return move