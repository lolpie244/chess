import copy

import chess_pieces.get_piece_positions_info
from chess_pieces.get_piece_positions_info import can_go


def is_check(board, color):
    opposite_color = 'white' if color == 'black' else 'black'
    for i in board.pieces[opposite_color]:
        if i.can_go_func(pos=board.kings[color].pos, board=board):
            return True
    return False


def is_mate(board, color):
    save_pieces = []
    if can_go(board.kings[color], board):
        return False
    opposite_color = 'white' if color == 'black' else 'black'
    count = 0
    for i in board.pieces[opposite_color]:
        if i.can_go_func(pos=board.kings[color].pos, board=board):
            count += 1
            if count == 2:
                return True
            save_pieces.extend(chess_pieces.get_piece_positions_info.get_overlap_positions(i.pos, board.kings[color].pos))
    if len(save_pieces) == 0:
        return False
    for i in board.pieces[color]:
        for j in save_pieces:
            if i.name == 'king':
                continue
            if i.can_go_func(pos=j, board=board):
                return False
    return True


def is_draw(board, color):
    if is_check(board, color):
        return False

    if can_go(board.kings[color], board):
        return False

    for i in board.pieces[color]:
        if can_go(i, board):
            return False

    return True


