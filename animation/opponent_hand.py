import copy
import pygame
import random

from .card import Card
from .shared_objects import SharedObjects
from .util import bring_to_front
from .assets import DECK

from . import constants as c


class OpponentHand():
    """
    The hand of an opponent player. Implements the
    same functions as PrimaryHand, but with different animations.
    """

    def __init__(self, x, y, spread=c.OPPONENT_SPREAD_PX, scale=c.OPPONENT_SPREAD_DECK_CARD_SCALE, card_surf=DECK):
        """
        x: x-position of center of deck
        y: y-position of center of deck
        spread: how many pixel in either direction is the maximum that a card's
            center should be
        scale: floating point value indication what proportion of the original
            surface pased in each card should be
        card_surf: (the surface will not be modified!) the card surface to use
            for each card in the deck (this is what is displayed for each card,
            despite the actual surface of the card)
        cards: a list of Card object which should be in this hand to begin with
        """
        self.x = x
        self.y = y
        self.spread = spread
        self.surface = card_surf.copy()
        self.scale = scale

        # Stores a list of dummy cards which represent the real cards (since
        # we don't want to show real card surfaces to player)
        self.cards = []

    def draw(self):
        """
        A card moves from the draw deck to this opponent's hand.
        """
        card = Card(DECK)

        # Append the real card to the real list of cards
        self.cards.append(card)

        SharedObjects.get_animatables().append(card)

        self.animate_move_cards(self.cards[:-1])

        num_cards = len(self.cards)

        # Move the card to draw deck position
        card.instant_move(c.DRAW_DECK_CENTER_X, c.DRAW_DECK_CENTER_Y)

        # Move the new card from draw deck to spread deck
        card.move(
            new_centerx=self.get_position_for_card(num_cards - 1, num_cards),
            new_centery=self.y,
            duration=c.MOVE_CARD_ANI_DURATION
        )

        card.scale(
            from_scale=c.DRAW_DECK_SCALE,
            to_scale=c.OPPONENT_SPREAD_DECK_CARD_SCALE,
            duration=c.MOVE_CARD_ANI_DURATION
        )

    def play(self, card, random_offset=True):
        """
        Pops the top card off of the stack.
        Parameters:
        -----------
        card: a Card object
        """
        if not len(self.cards):
            # There are no cards to play
            raise Exception

        old_card = self.cards[-1]

        x, y = old_card.rect.center
        card.instant_move(x, y)

        animatables = SharedObjects.get_animatables()

        animatables.remove(old_card)
        self.cards.remove(old_card)

        if card in animatables:
            animatables.remove(card)

        disposable_animatables = SharedObjects.get_disposable_animatables()
        disposable_animatables.append(card)

        if (random_offset):
            x_offset = random.randint(-c.RANDOM_PLAY_OFFSET_RANGE,
                                      c.RANDOM_PLAY_OFFSET_RANGE)
            y_offset = random.randint(-c.RANDOM_PLAY_OFFSET_RANGE,
                                      c.RANDOM_PLAY_OFFSET_RANGE)
        else:
            x_offset = 0
            y_offset = 0

        card.move(
            new_centerx=c.PLAY_DECK_CENTER_X + x_offset,
            new_centery=c.PLAY_DECK_CENTER_Y + y_offset,
            duration=c.MOVE_CARD_ANI_DURATION
        )

        card.scale(
            from_scale=c.OPPONENT_SPREAD_DECK_CARD_SCALE,
            to_scale=c.PLAY_DECK_SCALE,
            duration=c.MOVE_CARD_ANI_DURATION
        )

        self.animate_move_cards(self.cards)

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

    def animate_move_cards(self, cards):
        """
        Moves the selection of self.cards to the appropriate position based
        off of the number of cards in the deck at the moment.
        Parameters:
        -----------
        cards: a list of Cards from self.cards
        """
        num_cards = len(self.cards)

        # Move previously existing cards
        for i, card in enumerate(cards):
            card.move(
                new_centerx=self.get_position_for_card(i, num_cards),
                new_centery=self.y,
                duration=c.MOVE_CARD_ANI_DURATION
            )
