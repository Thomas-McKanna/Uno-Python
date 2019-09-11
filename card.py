import pygame

from animatable import Animatable

import constants as c


class Card(Animatable):
    """
    Represents a generic Uno card, which may be a color/value pair, or be a 
    special card.
    """

    def __init__(self, surface, scale=c.DEFAULT_CARD_SCALE, x=0, y=0, hidden=False):
        """
        Initializes an Uno card for play.
        Parameters:
        -----------
        surface: an image asset in the form of a pygame.Surface
        scale: option floating point value indiating what proportion of the
            original surface asset size the card should be
        x: x-position of the card
        y: y-position of the card
        hidden: optional argument indicating whether or not the card is shown
            on the screen
        """
        super(Card, self).__init__(surface, x, y, hidden)
        self.instant_scale(scale)
