from pygame import Color

import constants as c

from hand import Hand
from shared_objects import GameObjects

class Player:
    """
    Represents a player in a game of Uno.
    """

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

