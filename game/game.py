import copy
from game.board import Board
from game.game_states_check import is_mate, is_draw


class Game:
    color_turn = 'white'
    piece = None

    def __init__(self):
        self.board = Board()

    def set_start_position(self, new_pos):
        if self.board.check_color(new_pos, self.color_turn):
            self.piece = self.board[new_pos]
            return True
        return False

    def set_end_position(self, new_pos):
        if not self.board.try_move_piece(self.piece, new_pos):
            return False
        self.color_turn = 'black' if self.color_turn == 'white' else 'white'
        self.piece = None
        if not self.is_game():
            print('something wrong, i can feel it')
            return 'error'

        if is_draw(self.board, self.color_turn):
            return 'draw'

        if self.board[new_pos].name == 'pawn' and new_pos[0] in [0, 7]:
            return ['pawn', new_pos]
        return True

    def set_position(self, new_pos):
        if self.board.check_color(new_pos, self.color_turn):
            return self.set_start_position(new_pos)
        elif not self.piece is None:
            return self.set_end_position(new_pos)

    def is_game(self):
        return not is_mate(self.board, self.color_turn)
