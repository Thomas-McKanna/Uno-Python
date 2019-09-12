import copy
import pygame

from card import Card
from hand import Hand
from shared_objects import GameObjects
from util import bring_to_front

import constants as c


class OpponentHand(Hand):
    """
    The hand of an opponent player. Implements the
    same functions as PrimaryHand, but with different animations.
    """

    def __init__(self, x, y, spread, scale, card_surf, cards=None):
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
        super(OpponentHand, self).__init__(cards)

        self.x = x
        self.y = y
        self.spread = spread
        self.surface = card_surf.copy()
        self.scale = scale

        # Stores a list of dummy cards which represent the real cards (since
        # we don't want to show real card surfaces to player)
        self.cards = []

    def draw_card(self, card):
        """
        A card moves from the draw deck to this opponent's hand.
        Parameters:
        -----------
        card: the Card object to be added to this hand
        """
        # Append the real card to the real list of cards
        self.cards.append(card)

        GameObjects.get_animatables().append(card)

        self.animate_move_cards(self.cards[:-1])

        num_cards = len(self.cards)
        
        # Move the card to draw deck position
        card.instant_move(c.DRAW_DECK_CENTER_X, c.DRAW_DECK_CENTER_Y)

        # Flip that card (since it should be hidden)
        card.flip()

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

    def play_card(self, card=None):
        """
        Pops the top card off of the stack.
        Parameters:
        -----------
        card: a Card object which is in this Hand. The card will be removed
        from the hand.
        """
        if card is None:
            if len(self.cards):
                # default to playing the last card
                card = self.cards[-1]
            else:
                return None
            
        if not card in self.cards:
            return None

        # Bring card to the front of screen
        bring_to_front(card)

        # Flip the card over so that we can see its face
        card.flip()

        card.move(
            new_centerx=c.PLAY_DECK_CENTER_X,
            new_centery=c.PLAY_DECK_CENTER_Y,
            duration=c.MOVE_CARD_ANI_DURATION
        )

        card.scale(
            from_scale=c.OPPONENT_SPREAD_DECK_CARD_SCALE,
            to_scale=c.PLAY_DECK_SCALE,
            duration=c.MOVE_CARD_ANI_DURATION
        )

        self.cards.remove(card)

        self.animate_move_cards(self.cards)

        return card

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
