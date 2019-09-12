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

        self.focus_index = len(self.cards) // 2

        self.last_rotate_time = time.time()

        self.angle_offset_map = {}

        for card in self.cards:
            card.instant_scale(c.DEFAULT_CARD_SCALE)

    def arrange(self, scale_focus=False):
        """
        Moves hand into circular position at bottom of screen.
        """
        # Center
        self.cards[self.focus_index].move(
            c.FOCUS_CARD_X,
            c.FOCUS_CARD_Y,
            c.SHIFT_HAND_DURATION
        )
        self.angle_offset_map[self.cards[self.focus_index]] = 0

        angles = self._get_angles()

        # TODO: fix DRY violation below

        # Left side
        for i, card in enumerate(self.cards[:self.focus_index][::-1]):
            x, y = circle_transform(
                c.FOCUS_CARD_X,
                c.FOCUS_CARD_Y,
                c.HAND_CIRCLE_CENTER_X,
                c.HAND_CIRCLE_CENTER_Y,
                -angles[i]
            )
            self.angle_offset_map[card] = -angles[i]
            card.move(x, y, c.SHIFT_HAND_DURATION)

        # Right side
        for i, card in enumerate(self.cards[self.focus_index+1:]):
            x, y = circle_transform(
                c.FOCUS_CARD_X,
                c.FOCUS_CARD_Y,
                c.HAND_CIRCLE_CENTER_X,
                c.HAND_CIRCLE_CENTER_Y,
                angles[i]
            )
            self.angle_offset_map[card] = -angles[i]
            card.move(x, y, c.SHIFT_HAND_DURATION)

        if scale_focus:
            self.cards[self.focus_index].scale(
                c.DEFAULT_CARD_SCALE, c.FOCUS_CARD_SCALE)

    def rotate(self, right=True):
        """
        Rotates all cards in the hand clockwise.

        Parameters:
        -----------
        clockwise: True if rotating clockwise and False if rotating counter-
            clockwise
        """
        curr_time = time.time()

        if curr_time - self.last_rotate_time < c.SHIFT_HAND_DURATION + 2 / c.FPS:
            # Do not initiate a new rotation if already rotating
            return

        self.last_rotate_time = curr_time

        if right:
            if self.focus_index + 1 == len(self.cards):
                return
            else:
                self.cards[self.focus_index].scale(
                    c.FOCUS_CARD_SCALE,
                    c.DEFAULT_CARD_SCALE,
                    c.SHIFT_HAND_DURATION
                )
                self.focus_index += 1
                self.cards[self.focus_index].scale(
                    c.DEFAULT_CARD_SCALE,
                    c.FOCUS_CARD_SCALE,
                    c.SHIFT_HAND_DURATION
                )
        else:
            if self.focus_index == 0:
                return
            else:
                self.cards[self.focus_index].scale(
                    c.FOCUS_CARD_SCALE,
                    c.DEFAULT_CARD_SCALE,
                    c.SHIFT_HAND_DURATION
                )
                self.focus_index -= 1
                self.cards[self.focus_index].scale(
                    c.DEFAULT_CARD_SCALE,
                    c.FOCUS_CARD_SCALE,
                    c.SHIFT_HAND_DURATION
                )

        self.arrange()

    def _get_angles(self):
        """
        Returns a list for which each element indicates how many more degrees
        a card should be place beyond it's neighbor closest to the focus card.
        """
        # Number of cards on the side with the most cards on it (left or right)
        bigger_side_num = max(self.focus_index, len(
            self.cards) - self.focus_index + 1)

        # Each angle value will be slightly less
        fractions = [
            1/(i+2) for i in range(bigger_side_num)
        ]

        # Accumlate fractions to determine angles
        for i in range(1, len(fractions)):
            fractions[i] = fractions[i] + fractions[i - 1]

        # Determine angles based on fraction of boundary angle
        angles = []
        for fraction in fractions:
            angles.append(c.HAND_BOUNDARY_COEF * fraction)

        return angles
