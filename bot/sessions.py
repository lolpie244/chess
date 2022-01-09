import random
from aiogram import types
from game.game import Game


class Session:

    def __init__(self):
        self.game = Game()
        self.players = {'white': None, 'black': None}
        self.players_to_draw = []

    def player_join(self, player):
        if self.is_player(player):
            self.remove_player(player)
            return False
        if self.players['white'] is None and self.players['black'] is None:
            if random.randint(0, 1) == 0:
                self.players['white'] = player
            else:
                self.players['black'] = player
        elif self.players['white'] is None:
            self.players['white'] = player
        else:
            self.players['black'] = player
        return None not in self.players.values()

    def is_player(self, player):
        if self.players['white'] == player:
            return 'white'
        if self.players['black'] == player:
            return 'black'
        return None

    def get_player(self):
        return self.players[self.game.color_turn]

    def get_opposite_player(self):
        return self.players['white' if self.game.color_turn == 'black' else 'black']

    def remove_player(self, player):
        color = self.is_player(player)
        if color is None:
            return False
        self.players[color] = None
        return True

    def get_player_list(self, text, with_color=False):
        entities_list = []
        for color, player in self.players.items():
            if player is None:
                continue
            entities_list.append(
                types.MessageEntity('text_mention', offset=len(text), length=len(player.first_name),
                                    user=player))

            text += player.first_name + (('⚪️' if color == 'white' else '⚫️') if with_color else '') + '\n'

        return text, entities_list

    def player_draw(self, player):
        if player in self.players_to_draw:
            self.players_to_draw.remove(player)
            return False
        else:
            self.players_to_draw.append(player)
            if len(self.players_to_draw) == 2:
                return True
            return False


class Sessions:
    session_list = {}

    def add_session(self, message: types.Message):
        self.session_list[message.message_id] = Session()

    def __getitem__(self, item):
        return self.session_list[item.message_id]