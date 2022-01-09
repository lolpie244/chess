from aiogram import types


def board_keyboard(query, sessions, stage='game='):
    keys = [[] for _ in range(8)]
    matrix = sessions[query.inline_message_id].game.board.draw_board
    for i in range(8):
        for j in range(8):
            keys[i].append(types.InlineKeyboardButton(text=matrix[i][j], callback_data=f"{stage}{i},{j}"))
    return keys


def create_game():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Приєднатись до гри", callback_data="join_registration"))
    return "Гру в шахмати запущено", keyboard


def registration(query, sessions):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Приєднатись до гри", callback_data="join_registration"))
    text, entities = sessions[query.inline_message_id].get_player_list('Гравці: ')
    return text, keyboard, entities


def game(query, sessions):
    keyboard = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text="Нічия", callback_data="try_draw")
    key_2 = types.InlineKeyboardButton(text="Здатись", callback_data="surrender")
    keyboard.row(key_1, key_2)
    keys = board_keyboard(query, sessions)
    for i in range(8):
        keyboard.row(*keys[i])

    text, entities = sessions[query.inline_message_id].get_player_list('Гра триває. Гравці:\n', with_color=True)
    text += '\nЗараз ходить '
    player = sessions[query.inline_message_id].get_player()
    entities.append(types.MessageEntity('text_mention', offset=len(text), length=len(player.first_name),
                            user=player))
    text += player.first_name + ('⚪️' if sessions[query.inline_message_id].game.color_turn == 'white' else '⚫️')
    if len(sessions[query.inline_message_id].players_to_draw) == 1:
        player = sessions[query.inline_message_id].players_to_draw[0]
        text += '\n\n Гравець '
        entities.append(types.MessageEntity('text_mention', offset=len(text), length=len(player.first_name),
                                            user=player))
        text += player.first_name + ' пропонує нічию'

    return text, keyboard, entities


def choose_pawn(query, sessions, pos):
    piece_text = {'white': {
        'queen': '♕', 'knight': '♘', 'rook': '♖', 'bishop': '♗'
    }, 'black': {
        'queen': '♛', 'knight': '♞', 'rook': '♜', 'bishop': '♝'
    }}
    keyboard = types.InlineKeyboardMarkup()
    keys = []
    for i, val in piece_text[sessions[query.inline_message_id].game.board[pos].color].items():
        keys.append(types.InlineKeyboardButton(text=val, callback_data=f"choose={i}={pos[0]},{pos[1]}"))
    keyboard.row(*keys)
    keys = [types.InlineKeyboardButton(text=' ', callback_data=f'choose=1,2') for _ in range(4)]
    keyboard.row(*keys)
    keys = board_keyboard(query, sessions, 'choose=')
    for i in range(8):
        keyboard.row(*keys[i])

    text, entities = sessions[query.inline_message_id].get_player_list('Гра триває. Гравці:\n', with_color=True)
    text += '\nЗараз ходить '
    player = sessions[query.inline_message_id].get_player()
    entities.append(types.MessageEntity('text_mention', offset=len(text), length=len(player.first_name),
                                        user=player))
    text += player.first_name + ('⚪️' if sessions[query.inline_message_id].game.color_turn == 'white' else '⚫️')

    return text, keyboard, entities


def end_game(query, sessions):
    keyboard = types.InlineKeyboardMarkup()
    keys = board_keyboard(query, sessions, 'nothing=')
    for i in range(8):
        keyboard.row(*keys[i])
    text, entities = sessions[query.inline_message_id].get_player_list('Гравці:\n', with_color=True)
    color = 'black' if sessions[query.inline_message_id].game.color_turn == 'white' else 'white'
    player = sessions[query.inline_message_id].players[color]
    text += '\nШах і мат. Переможець - '
    entities.append(types.MessageEntity('text_mention', offset=len(text), length=len(player.first_name),
                                        user=player))
    text += player.first_name + ('⚪️' if color == 'white' else '⚫️')
    return text, keyboard, entities


def draw_game(query, sessions):
    keyboard = types.InlineKeyboardMarkup()
    keys = board_keyboard(query, sessions, 'nothing=')
    for i in range(8):
        keyboard.row(*keys[i])
    text, entities = sessions[query.inline_message_id].get_player_list('Гравці:\n', with_color=True)
    text += '\nНічия'
    return text, keyboard, entities


def surrender(query, sessions):
    keyboard = types.InlineKeyboardMarkup()
    keys = board_keyboard(query, sessions, 'nothing=')
    for i in range(8):
        keyboard.row(*keys[i])
    text, entities = sessions[query.inline_message_id].get_player_list('Гравці:\n', with_color=True)
    color = 'black' if sessions[query.inline_message_id].game.color_turn == 'white' else 'white'
    player = sessions[query.inline_message_id].players['black'] if sessions[query.inline_message_id].players['black'].id == query.from_user.id else 'white'
    player = None
    if sessions[query.inline_message_id].players['black'].id == query.from_user.id:
        player = sessions[query.inline_message_id].players['black']
    else:
        player = sessions[query.inline_message_id].players['white']
    text += '\nГравець '
    entities.append(types.MessageEntity('text_mention', offset=len(text), length=len(player.first_name),
                                        user=player))
    text += player.first_name + ' здався'
    return text, keyboard, entities