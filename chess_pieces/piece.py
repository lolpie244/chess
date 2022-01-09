import copy
import functools
from chess_pieces.rules import check


class Piece:
    name = ''
    color = 'white'

    def get_opposite_color(self):
        return 'w' if self.color == 'black' else 'b'

    def __init__(self, new_pos: (0, 0), piece_type, color, additional=None):
        self.additional = {}
        if additional is not None:
            self.additional = additional
        self.pos = list(copy.deepcopy(new_pos))
        self.name = piece_type
        self.color = color

    def can_go_func(self, pos, board, return_additional=False):
        return check(self, pos, board, return_additional)