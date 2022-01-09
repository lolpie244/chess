import copy


def additional_check(pos, new_pos, board):
    i, j = pos[0], pos[1]
    n, m = new_pos[0], new_pos[1]
    func = lambda a, b: a + (1 if a < b else -1 if a > b else 0)
    ans = []
    n = func(n, i)
    m = func(m, j)
    while i != n or j != m:
        if board[[n, m]] is not None:
            return False
        n = func(n, i)
        m = func(m, j)
    return True


def king(piece, pos, board):
    self_pos = piece.pos
    additional = copy.deepcopy(piece.additional)
    additional['had_moved'] = True
    if not piece.additional['had_moved']:
        if self_pos[0] - pos[0] == 0 and abs(self_pos[1] - pos[1]) == 2:
            rook_, rook_pos = (board[[pos[0], 0]], [self_pos[0], self_pos[1] - 1]) if self_pos[1] - pos[1] == 2 else \
                (board[[pos[0], 7]], [self_pos[0], self_pos[1] + 1])
            if rook_.additional['had_moved'] or not additional_check(rook_.pos, self_pos, board):
                return False, additional
            additional['special'] = f'self.move_piece(self.__getitem__({rook_.pos}), {rook_pos})'
            return True, additional

    return max(abs(pos[0] - self_pos[0]), abs(pos[1] - self_pos[1])) == 1 \
           and not board.check_color(pos, piece.color), additional


def queen(piece, pos, board):
    self_pos = piece.pos
    additional = copy.deepcopy(piece.additional)
    return (abs(pos[0] - self_pos[0]) == abs(pos[1] - self_pos[1]) or pos[0] == self_pos[0] or pos[1] == self_pos[1]) \
           and not board.check_color(pos, piece.color) and additional_check(self_pos, pos, board), additional


def bishop(piece, pos, board):
    self_pos = piece.pos
    additional = copy.deepcopy(piece.additional)
    return (abs(pos[0] - self_pos[0]) == abs(pos[1] - self_pos[1])) and not board.check_color(pos, piece.color) \
           and additional_check(self_pos, pos, board), additional


def knight(piece, pos, board):
    self_pos = piece.pos
    additional = copy.deepcopy(piece.additional)
    temp = (abs(self_pos[0] - pos[0]), abs(self_pos[1] - pos[1]))
    return (temp == (1, 2) or temp == (2, 1)) and not board.check_color(pos, piece.color), additional


def rook(piece, pos, board):
    self_pos = piece.pos
    additional = copy.deepcopy(piece.additional)
    return (pos[0] == self_pos[0] or pos[1] == self_pos[1]) and not board.check_color(pos, piece.color) \
           and additional_check(self_pos, pos, board), additional


def pawn(piece, pos, board):
    self_pos = piece.pos
    additional = copy.deepcopy(piece.additional)
    opposite_color = 'black' if piece.color == 'white' else 'white'
    j = -1 if piece.color == 'white' else 1
    k = 6 if piece.color == 'white' else 1
    if not board.check_color(pos, piece.color):
        if board[pos] is None and pos[1] - self_pos[1] == 0 and self_pos[0] == k and pos[0] - self_pos[0] == j * 2:
            additional['double_turn'] = board.turn_count
        else:
            additional['double_turn'] = 0
        if board[pos] is None and pos[0] - self_pos[0] == j and abs(pos[1] - self_pos[1]) == 1 \
                and board.check_color(pos, opposite_color) and \
                board[[self_pos[0], pos[1]]].additional.get('double_turn', 0) - board.turn_count == 1:
            additional['special'] = f'self.remove_piece({[self_pos[0], pos[1]]})'
            return True, additional

        return board[pos] is None and pos[1] - self_pos[1] == 0 and (self_pos[0] == k and pos[0] - self_pos[0] == j * 2
                                                                     or pos[0] - self_pos[0] == j) \
               or pos[0] - self_pos[0] == j and abs(pos[1] - self_pos[1]) == 1 \
               and board.check_color(pos, opposite_color), additional


def check(piece, pos, board, return_additional=False):
    temp = {'king': king, 'queen': queen, 'bishop': bishop, 'knight': knight, 'rook': rook, 'pawn': pawn}
    ans = temp[piece.name](piece, pos, board)
    if return_additional:
        return ans
    return ans[0]
