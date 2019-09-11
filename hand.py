from card import Card
from util import circle_transform
from constants import HAND_CIRCLE_CENTER_X, HAND_CIRCLE_CENTER_Y, FOCUS_CARD_SCALE, DEFAULT_CARD_SCALE, FOCUS_CARD_X, FOCUS_CARD_Y, ROTATE_HAND_DURATION, FPS

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

        self.focus_index = 0
        self.last_rotate_time = time.time()

        for card in self.cards:
            card.instant_scale(DEFAULT_CARD_SCALE)

    def arrange(self):
        """
        Moves hand into circular position at bottom of screen.
        """
        num_cards = len(self.cards)
        angles = [
            (360 / num_cards) * i for i in range(num_cards)
        ]

        i = 0
        while i < num_cards:
            x, y = circle_transform(
                FOCUS_CARD_X,
                FOCUS_CARD_Y,
                HAND_CIRCLE_CENTER_X,
                HAND_CIRCLE_CENTER_Y,
                angles[i]
            )
            self.cards[(self.focus_index + i) % num_cards].move(x, y)
            i += 1

        self.cards[self.focus_index].scale(
            DEFAULT_CARD_SCALE, FOCUS_CARD_SCALE)

    def rotate(self, clockwise=True):
        """
        Rotates all cards in the hand clockwise.

        Parameters:
        -----------
        clockwise: True if rotating clockwise and False if rotating counter-
            clockwise
        """
        curr_time = time.time()

        if curr_time - self.last_rotate_time < ROTATE_HAND_DURATION + 2 / FPS:
            # Do not initiate a new rotation if already rotating
            return

        self.last_rotate_time = curr_time

        if clockwise:
            cw = 1
        else:
            cw = -1

        if len(self.cards) <= 1:
            # Don't rotate if there is only one card left
            return

        # Rotate each card in hand
        angle_to_rotate = 360 / len(self.cards)
        for card in self.cards:
            card.circle(
                center_x=HAND_CIRCLE_CENTER_X,
                center_y=HAND_CIRCLE_CENTER_Y,
                angle=cw * angle_to_rotate,
                duration=ROTATE_HAND_DURATION)

        # Scale down the old focus card
        self.cards[self.focus_index].scale(
            from_scale=FOCUS_CARD_SCALE,
            to_scale=DEFAULT_CARD_SCALE,
            duration=ROTATE_HAND_DURATION
        )

        # Set new focus card
        self.focus_index = (self.focus_index - cw) % len(self.cards)

        # Scale up the new focus card
        self.cards[self.focus_index].scale(
            from_scale=DEFAULT_CARD_SCALE,
            to_scale=FOCUS_CARD_SCALE,
            duration=ROTATE_HAND_DURATION
        )
