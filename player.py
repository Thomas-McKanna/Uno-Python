from pygame import Color

import constants as c

from hand import Hand
from shared_objects import GameObjects

class Player:
    """
    Represents a player in a game of Uno.
    """
    # Static member which holds reference to list of last played cards (used to 
    # delete animatable which is no longer needed)
    last_played_cards = []

    def __init__(self, name):
        """
        Parameters:
        -----------
        name: string name for the player
        """
        self.name = name

    def get_name_surface(self, color=c.FONT_COLOR):
        """
        Returns a surface with the player's name rendered on it.
        """
        font = GameObjects.get_font()
        surface = font.render(self.name, True, color)
        return surface

    def get_last_played_cards(self):
        return Player.last_played_cards

    def push_last_played_card(self, card):
        Player.last_played_cards.append(card)

    def pop_last_played_card(self):
        Player.last_played_cards.pop()

