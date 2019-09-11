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

    def push_card(self):
        """
        Animates a card moving to the deck. The new card is hidden and the
        function show_top_card will subsequently have to be called in order
        to show the card (it is automatically hidden so that as the card
        goes from draw deck to spread deck there are not two representations
        of it on the screen).
        """
        new_card = Card(
            self.surface,
            c.DRAW_DECK_SCALE,
            c.DRAW_DECK_CENTER_X,
            c.DRAW_DECK_CENTER_Y
        )

        self.cards.append(new_card)

        GameObjects.get_animatables().append(new_card)

        self.animate_move_cards(self.cards[:-1])

        num_cards = len(self.cards)

        # Move the new card from draw deck to spread deck
        new_card.move(
            new_centerx=self.get_position_for_card(num_cards - 1, num_cards),
            new_centery=self.y,
            duration=c.OPPONENT_SPREAD_DECK_ANI_DURATION
        )

        new_card.scale(
            from_scale=c.DRAW_DECK_SCALE,
            to_scale=c.OPPONENT_SPREAD_DECK_CARD_SCALE,
            duration=c.OPPONENT_SPREAD_DECK_ANI_DURATION
        )

    def pop_card(self, card_surface):
        """
        Pops the top card off of the stack.
        Parameters:
        -----------
        card_surface: the card_surface to reveal and move to the play deck
        Returns:
        --------
        The newly created play card, which should be removed from animatables
        at the proper time (after next play card)
        """
        if not len(self.cards):
            return

        old_card = self.cards[-1]
        x, y = old_card.rect.center
        play_card = Card(
            card_surface,
            scale=1,
            x=x,
            y=y
        )

        animatables = GameObjects.get_animatables()

        # TODO: this temporary card never gets removed from animatables list,
        # and so subsequent card plays will slowly bog down the system. It
        # needs to be removed from animatables after the animation completes.
        animatables.append(play_card)

        play_card.move(
            new_centerx=c.PLAY_DECK_CENTER_X,
            new_centery=c.PLAY_DECK_CENTER_Y,
            duration=c.OPPONENT_SPREAD_DECK_ANI_DURATION
        )

        play_card.scale(
            from_scale=c.OPPONENT_SPREAD_DECK_CARD_SCALE,
            to_scale=c.PLAY_DECK_SCALE,
            duration=c.OPPONENT_SPREAD_DECK_ANI_DURATION
        )

        animatables.remove(old_card)
        self.cards.pop()

        self.animate_move_cards(self.cards)

        return play_card

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
                duration=c.OPPONENT_SPREAD_DECK_ANI_DURATION
            )
