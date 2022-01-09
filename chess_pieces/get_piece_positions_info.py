from chess_pieces.rules import check


def get_overlap_positions(pos, new_pos, piece=''):
    if piece in ['knight', 'pawn']:
        return [pos]

    i, j = pos[0], pos[1]
    n, m = new_pos[0], new_pos[1]
    func = lambda a, b: a + (1 if a < b else -1 if a > b else 0)
    ans = []
    while i != n or j != m:
        ans.append([i, j])
        i = func(i, n)
        j = func(j, m)
    return ans


def knight(piece, board):
    self_pos = piece.pos
    for i in range(-1, 2, 2):
        for j in range(-1, 2, 2):
            pos = [self_pos[0] + i, self_pos[1] + 2 * j]
            if board.try_move_piece(piece, pos, True):
                return True
            pos = [self_pos[0] + 2 * i, self_pos[1] + j]
            if board.try_move_piece(piece, pos, True):
                return True
    return False


def king(piece, board):
    king_pos = board.kings[piece.color].pos
    for i in range(-1, 2):
        for j in range(-1, 2):
            new_pos = [king_pos[0] + i, king_pos[1] + j]
            if i == 0 and j == 0:
                continue
            if board.try_move_piece(piece, new_pos, True):
                return True
    return False


def pawn(piece, board):
    j = -1 if piece.color == 'white' else 1
    pos = piece.pos
    return board.try_move_piece(piece, [pos[0] + j, pos[1]], True) or \
           board.try_move_piece(piece, [pos[0] + 2 * j, pos[1]], True) or \
           board.try_move_piece(piece, [pos[0] + j, pos[1] + 1], True) or \
           board.try_move_piece(piece, [pos[0] + j, pos[1] + 1], True)


def rook(piece, board):
    pos = piece.pos
    for i in range(-8, 8):
        if i == 0:
            continue
        if board.try_move_piece(piece, [pos[0] + i, pos[1]], True):
            return True
        if board.try_move_piece(piece, [pos[0], pos[1] + i], True):
            return True
    return False


def bishop(piece, board):
    pos = piece.pos
    for k in range(1, 8):
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                if board.try_move_piece(piece, [pos[0] + i * k, pos[1] + j * k], True):
                    return True
    return False


def queen(piece, board):
    return rook(piece, board) or bishop(piece, board)


def can_go(piece, board):
    list_ = {'king': king, 'queen': queen, 'bishop': bishop, 'knight': knight, 'rook': rook, 'pawn': pawn}
    return list_[piece.name](piece, board)
