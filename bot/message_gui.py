from aiogram import types

from bot import messages


async def registration_gui(bot, sessions, query: types.CallbackQuery):
    text, keyboard, entities = messages.registration(query, sessions)
    await bot.edit_message_text(text=text, inline_message_id=query.inline_message_id, reply_markup=keyboard, entities=entities)


async def game_gui(bot, sessions, query: types.CallbackQuery):
    text, keyboard, entities = messages.game(query, sessions)
    await bot.edit_message_text(text=text, inline_message_id=query.inline_message_id, reply_markup=keyboard,
                                entities=entities)


async def end_gui(bot, sessions, query: types.CallbackQuery):
    text, keyboard, entities = messages.end_game(query, sessions)
    await bot.edit_message_text(text=text, inline_message_id=query.inline_message_id, reply_markup=keyboard,
                                entities=entities)


async def surrender_gui(bot, sessions, query: types.CallbackQuery):
    text, keyboard, entities = messages.surrender(query, sessions)
    await bot.edit_message_text(text=text, inline_message_id=query.inline_message_id, reply_markup=keyboard,
                                entities=entities)


async def choose_gui(bot, sessions, query: types.CallbackQuery, pos):
    text, keyboard, entities = messages.choose_pawn(query, sessions, pos)
    await bot.edit_message_text(text=text, inline_message_id=query.inline_message_id, reply_markup=keyboard,
                                entities=entities)


async def draw_gui(bot, sessions, query: types.CallbackQuery):
    text, keyboard, entities = messages.draw_game(query, sessions)
    await bot.edit_message_text(text=text, inline_message_id=query.inline_message_id, reply_markup=keyboard,
                                entities=entities)