from card import Card
from util import circle_transform
import constants as c
from shared_objects import GameObjects

import time


class Hand:
    """
    Manages a set of cards.
    """
    def __init__(self, cards=None):
        if cards is not None:
            self.cards = cards
        else:
            self.cards = []
