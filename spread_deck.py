import copy
import pygame

from card import Card
from shared_objects import GameObjects
import constants as c


class SimpleSpreadDeck:
    """
    A horizontal set of cards which expands and shrink according to its size.
    It is called "simple" because all of the cards are of the same type and 
    cards can only be added or taken away from the front of the deck.

    Note that this deck is really just for cosmetic purposes.
    """

    def __init__(self, x, y, spread, scale, card_surf, num_cards=0):
        """
        x: x-position of center of deck
        y: y-position of center of deck
        spread: how many pixel in either direction is the maximum that a card's
            center should be
        scale: floating point value indication what proportion of the original
            surface pased in each card should be
        card_surf: (the surface will not be modified!) the card surface to use
            for each card in the deck
        num_cards: optional value indication how many cards should be in the
            deck to start
        """
        self.x = x
        self.y = y
        self.spread = spread
        self.surface = card_surf.copy()
        self.scale = scale

        self.cards = []
        for _ in range(num_cards):
            self.add_card()

    def add_card(self):
        """
        Animates a card moving to the deck.
        """
        new_card = Card(self.surface, self.scale, c.HALF_WINWIDTH, c.HALF_WINHEIGHT)

        self.cards.append(new_card)

        GameObjects.get_animatables().append(new_card)

        for i, card in enumerate(self.cards):
            card.move(
                new_centerx=self.get_position_for_card(i, len(self.cards)),
                new_centery=self.y,
                duration=c.OPPONENT_SPREAD_DECK_ANI_DURATION
            )

    def get_position_for_card(self, position, num_cards):
        """
        Given a position of the card and the total number of cards in the deck,
        returns the x coordinate of the card (since y is constant)
        Parameters:
        -----------
        position: the numeric position of the card (0 is first card)
        num_cards: the number of cards in the deck
        """
        start = self.x - self.spread
        x = start + round((position+1)/(num_cards+1) * (self.spread*2))
        return x
