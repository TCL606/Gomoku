from tkinter import *
from tkinter import messagebox
from .game import Game
from player import Player
from state import Board 
import threading

class GUIGame(Game):
    def __init__(self, board: Board, **kwargs):
        super().__init__(board, **kwargs)
        self.root = Tk()
        self.root.title('Gomoku')
        self.C = board.width
        self.R = board.height
        self.cell_size = 30
        self.height = self.R * self.cell_size
        self.width = self.C * self.cell_size
        self.cv = Canvas(self.root, height=self.height, width=self.width)
        self.cv.pack()
        self.color_now = ("#FFFFFF", "#000000")
        self.board_shift_x = 0.5
        self.board_shift_y = 0.5

        self.draw_board(self.C, self.R)


    def draw_cell(self, c, r, color="#CCCCCC"):
        x0 = c * self.cell_size
        y0 = r * self.cell_size
        x1 = x0 + self.cell_size
        y1 = y0 + self.cell_size
        self.cv.create_rectangle(x0, y0, x1, y1, fill=color, outline="white", width=2)
    
    def draw_board(self, x, y):
        for ci in range(x - 1):
            for ri in range(y - 1):
                self.draw_cell(ci + self.board_shift_x, ri + self.board_shift_y)
    
    def draw_chequer(self, x, y, color="#000000"):
        x = x + self.board_shift_x
        y = y + self.board_shift_y
        c = x * self.cell_size
        r = y * self.cell_size
        x0 = int(c - self.cell_size / 2)
        y0 = int(r - self.cell_size / 2)
        x1 = int(x0 + self.cell_size)
        y1 = int(y0 + self.cell_size)
        self.cv.create_oval(x0, y0, x1, y1, fill=color)

    def graphic(self, board: Board, player1, player2):
        if board.get_last_move() != -1:
            [x, y] = board.move_to_location(board.get_last_move())
            current_player = board.get_current_player()  # actually, this is the player who will move next
            color = self.color_now[0] if current_player == player1 else self.color_now[1]
            self.draw_chequer(x, y, color)

    def start_play(self, player1: Player, player2: Player, start_player=0, is_shown=1):
        def run_in_thread(player1, player2, start_player, is_shown):
            if start_player not in (0, 1):
                raise Exception('start_player should be either 0 (player1 first) '
                                'or 1 (player2 first)')
            self.board.reset(start_player)
            p1, p2 = self.board._players
            player1.set_player(p1)
            player2.set_player(p2)
            players = {p1: player1, p2: player2}
            if is_shown:
                self.graphic(self.board, player1.player, player2.player)
            while True:
                current_player = self.board.get_current_player()
                player_in_turn = players[current_player]
                move = player_in_turn.get_action(self.board)
                # print(self.board.move_to_location(move))
                self.board.perform_action(move)
                if is_shown:
                    self.graphic(self.board, player1.player, player2.player)
                end, winner = self.board.game_end()
                if end:
                    if is_shown:
                        if winner != -1:
                            messagebox.showinfo("info", f"Game end. Winner is {players[winner]}")
                        else:
                            messagebox.showinfo("info", "Game end. Tie")
                    self.root.quit()
                    return winner
                
        t = threading.Thread(target=run_in_thread, args=(player1, player2, start_player, is_shown), daemon=True)
        t.start()
        self.root.mainloop()

    
    def correct_mouse(self, x, y):
        def correct(x):
            if x < self.cell_size:
                return self.cell_size
            if x > (self.R - 1) * self.cell_size:
                return (self.R - 1) * self.cell_size
            xa = int(x / self.cell_size)
            xb = x % self.cell_size
            if xb >= self.cell_size / 2:
                return int(xa * self.cell_size + self.cell_size)
            else:
                return int(xa * self.cell_size)
            
        return correct(x), correct(y)