import copy

from chess_pieces.piece import Piece
from game.game_states_check import is_check


class Board:

    def fill_side(self, color):
        k = 0 if color == 'black' else 7
        j = 1 if color == 'black' else 6
        for i in range(8):
            self.add_piece(Piece((j, i), 'pawn', color, {'moved_double': False}))
        self.add_piece(Piece((k, 1), 'knight', color))
        self.add_piece(Piece((k, 6), 'knight', color))
        self.add_piece(Piece((k, 4), 'king', color, {'had_moved': False}))
        self.add_piece(Piece((k, 5), 'bishop', color))
        self.add_piece(Piece((k, 2), 'bishop', color))
        self.add_piece(Piece((k, 0), 'rook', color, {'had_moved': False}))
        self.add_piece(Piece((k, 7), 'rook', color, {'had_moved': False}))
        self.add_piece(Piece((k, 3), 'queen', color))

    def __init__(self):
        self.turn_count = 0
        self.pieces = {'white': [], 'black': []}
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.draw_board = [[' ' for _ in range(8)] for _ in range(8)]
        self.fill_side('white')
        self.fill_side('black')
        self.kings = {'white': self.__getitem__([7, 4]), 'black': self.__getitem__([0, 4])}

    def make_snap(self, piece, new_pos):
        snap = {'removed': copy.deepcopy(self.__getitem__(new_pos)), 'old_pos': copy.deepcopy(piece.pos),
                'piece': piece, 'new_pos': copy.deepcopy(new_pos),
                'removed_draw': self.draw_board[new_pos[0]][new_pos[1]]}
        return snap

    def load_snap(self, snap):
        self.draw_board[snap['old_pos'][0]][snap['old_pos'][1]] = self.draw_board[snap['new_pos'][0]][snap['new_pos'][1]]
        self.draw_board[snap['new_pos'][0]][snap['new_pos'][1]] = snap['removed_draw']
        self.add_piece(snap['removed'])
        self.__setitem__(snap['old_pos'], snap['piece'])
        self.__setitem__(snap['new_pos'], snap['removed'])
        snap['piece'].pos = snap['old_pos']

    def move_piece(self, piece, new_pos):
        self.remove_piece(new_pos)
        old_pos = copy.deepcopy(piece.pos)
        piece.pos = copy.deepcopy(new_pos)
        self.__setitem__(piece.pos, piece)
        self.__setitem__(old_pos, None)
        self.draw_board[new_pos[0]][new_pos[1]] = self.draw_board[old_pos[0]][old_pos[1]]
        self.draw_board[old_pos[0]][old_pos[1]] = ' '

    def try_move_piece(self, piece, new_pos, is_try=False):
        if not(0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7):
            return False
        # print(piece.name, piece.pos, new_pos)
        f, additional = piece.can_go_func(new_pos, self, True)
        if not f:
            return False
        snap = self.make_snap(piece, new_pos)
        self.move_piece(piece, new_pos)
        if is_check(self, piece.color):
            self.load_snap(snap)
            return False
        if not is_try:
            val = additional.pop('special', None)
            if val is not None:
                eval(val)
            piece.additional = additional
        else:
            self.turn_count += 1
            self.load_snap(snap)
        return True

    def remove_piece(self, pos):
        val = self.__getitem__(pos)
        if val is not None:
            self.draw_board[pos[0]][pos[1]] = ' '
            self.__setitem__(pos, None)
            self.pieces[val.color].remove(val)
            return

    def add_piece(self, piece):
        text = {'white': {
            'pawn': '♙', 'king': '♔', 'queen': '♕', 'knight': '♘', 'rook': '♖', 'bishop': '♗'
        }, 'black': {
            'pawn': '♟', 'king': '♚', 'queen': '♛', 'knight': '♞', 'rook': '♜', 'bishop': '♝'
        }}
        if piece is None:
            return
        self.pieces[piece.color].append(piece)
        self.draw_board[piece.pos[0]][piece.pos[1]] = copy.deepcopy(text[piece.color][piece.name])
        self.__setitem__(piece.pos, self.pieces[piece.color][len(self.pieces[piece.color]) - 1])

    def check_color(self, pos, color):
        val = self.__getitem__(pos)
        if val is None:
            return False
        return val.color == color

    def __getitem__(self, item):
        return self.board[item[0]][item[1]]

    def __setitem__(self, key, value):
        self.board[key[0]][key[1]] = value
