import pygame
import math
import copy
from numpy import arange
from util import checkForKeyPress
from shared_objects import GameObjects
from constants import FPS
from animatable import Animatable


class Card(Animatable):
    WIDTH = 97  # width in pixels
    HEIGHT = 140  # height in pixels

    def __init__(self, surface, x=0, y=0, hidden=False):
        """
        Initializes an Uno card for play.
        Parameters:
        -----------
        surface: an image asset in the form of a pygame.Surface
        """
        super(Card, self).__init__(surface, x, y, hidden)
