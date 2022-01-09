from aiogram import Bot, Dispatcher, executor, types
import token
from game.game_states_check import is_draw
from message_gui import game_gui, end_gui, choose_gui, draw_gui, registration_gui, surrender_gui
from sessions import Sessions
from chess_pieces import piece

token = token.get_token()
bot = Bot(token)
dp = Dispatcher(bot)
sessions = Sessions()


@dp.message_handler(commands=['start'])
async def create_game(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Приєднатись до гри", callback_data="join_registration"))
    sessions.add_session(await message.answer("Гру в шахмати запущено", reply_markup=keyboard))


@dp.callback_query_handler(text='join_registration')
async def add_player(query: types.CallbackQuery):
    if sessions[query.message].player_join(query.from_user):
        await game_gui(bot, sessions, query)
        return
    await registration_gui(bot, sessions, query)


@dp.callback_query_handler(text='surrender')
async def surrender(query: types.CallbackQuery):
    if not sessions[query.message].is_player(query.from_user):
        return await query.answer(text='це не ваша гра')
    return await surrender_gui(bot, sessions, query)


@dp.callback_query_handler(text='try_draw')
async def try_draw(query: types.CallbackQuery):
    if not sessions[query.message].is_player(query.from_user):
        return await query.answer(text='це не ваша гра')
    if sessions[query.message].player_draw(query.from_user):
        return await draw_gui(bot, sessions, query)
    try:
        await game_gui(bot, sessions, query)
    except:
        pass


@dp.callback_query_handler()
async def game(query: types.CallbackQuery):
    stage = list(query.data.split('='))[0]
    stage_list = {'game': game_stage, 'choose': choose_stage, 'nothing': nothing_stage, 'draw': nothing_stage}
    return await stage_list[stage](query)


async def nothing_stage(query: types.CallbackQuery):
    return await query.answer(text='ця гра завершилась')


async def game_stage(query: types.CallbackQuery):
    if sessions[query.message].get_player().id != query.from_user.id:
        return await query.answer(text='це не ваш хід')

    pos = list(map(int, list(query.data.split('='))[1].split(',')))
    ret = sessions[query.message].game.set_position(pos)
    if not ret:
        await query.answer(text='неправильний хід')
        return
    try:
        await game_gui(bot, sessions, query)
    except:
        pass
    if ret == 'error':
        await end_gui(bot, sessions, query)
    if type(ret) == list and ret[0] == 'pawn':
        await choose_gui(bot, sessions, query, ret[1])


async def choose_stage(query: types.CallbackQuery):
    if sessions[query.message].get_player().id == query.from_user.id:
        return await query.answer(text='це не ваш хід')

    piece_name = list(query.data.split('='))[1]
    try:
        pos = list(map(int, list(query.data.split('='))[2].split(',')))
    except:
        return await query.answer(text='оберіть фігуру')
    board = sessions[query.message].game.board
    color = board[pos].color
    board.remove_piece(pos)
    board.add_piece(piece.Piece(pos, piece_name, color))
    if not sessions[query.message].game.is_game():
        await end_gui(bot, sessions, query)
        return await nothing_stage(query)

    if is_draw(sessions[query.message].game.board, sessions[query.message].game.color_turn):
        await draw_gui(bot, sessions, query)
        return await nothing_stage(query)

    await game_gui(bot, sessions, query)
    return




if __name__ == '__main__':
    executor.start_polling(dp)

