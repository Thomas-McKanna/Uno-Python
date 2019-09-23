import pygame
import copy

from .animatable import Animatable
from .assets import DECK

from . import constants as c


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
        self.face_surface = surface
        self.face_up = True
        super(Card, self).__init__(surface, x, y, hidden)
        self.instant_scale(scale)

    def flip(self):
        """
        Flips the card over; if the face is currently showing, then the back of
        the card (with logo) will be shown. If the back of the card is showing,
        then the face of the card (with number/color) will be shown.
        """
        self.face_up = not self.face_up

        if self.face_up:
            self.original_surface = self.face_surface.copy()
            self.instant_scale(self.current_scale)
        else:
            self.original_surface = DECK.copy()
            self.instant_scale(self.current_scale)
            

