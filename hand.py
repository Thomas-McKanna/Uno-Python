from card import Card
from util import circle_transform
import constants as c
from shared_objects import GameObjects

import time


class Hand:
    """
    Manages a set of cards.
    """

    def __init__(self, cards):
        self.cards = cards
        self.focus_index = len(self.cards) // 2
        self.last_rotate_time = time.time()

        self.angle_offset_map = {}

        for card in self.cards:
            card.instant_scale(c.DEFAULT_CARD_SCALE)

    def arrange(self):
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

        angles = self._get_angle_steps()

        # Accumlate value for each angle
        for i in range(1, len(angles)):
            angles[i] = angles[i] + angles[i - 1]

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

        self.cards[self.focus_index].scale(
            c.DEFAULT_CARD_SCALE, c.FOCUS_CARD_SCALE)

    def _layer_cards(self):
        """
        Removes all cards in the hand from the list of animatables and puts
        them back in order so that they layer nicely.
        """
        animatables = GameObjects.get_animatables()
        for card in self.cards:
            animatables.remove(card)
        for card in self.cards:
            animatables.push(card)

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

        # if clockwise:
        #     cw = 1
        # else:
        #     cw = -1

        # if len(self.cards) <= 1:
        #     # Don't rotate if there is only one card left
        #     return

        # # Rotate each card in hand
        # angle_to_rotate = 360 / len(self.cards)
        # for card in self.cards:
        #     card.circle(
        #         center_x=c.HAND_CIRCLE_CENTER_X,
        #         center_y=c.HAND_CIRCLE_CENTER_Y,
        #         angle=cw * angle_to_rotate,
        #         duration=c.SHIFT_HAND_DURATION)

        # # Scale down the old focus card
        # self.cards[self.focus_index].scale(
        #     from_scale=c.FOCUS_CARD_SCALE,
        #     to_scale=c.DEFAULT_CARD_SCALE,
        #     duration=c.SHIFT_HAND_DURATION
        # )

        # # Set new focus card
        # self.focus_index = (self.focus_index - cw) % len(self.cards)

        # # Scale up the new focus card
        # self.cards[self.focus_index].scale(
        #     from_scale=c.DEFAULT_CARD_SCALE,
        #     to_scale=c.FOCUS_CARD_SCALE,
        #     duration=c.SHIFT_HAND_DURATION
        # )

    def _get_angle_steps(self):
        """
        Returns a list for which each element indicates how many more degrees
        a card should be place beyond it's neighbor closest to the focus card.
        """
        # Number of cards on the side with the most cards on it (left or right)
        bigger_side_num = max(self.focus_index, len(
            self.cards) - self.focus_index + 1)

        # Each angle value will be slightly less
        angles_steps = [
            (c.HAND_BOUNDARY_ANGLE / ((i + 1)*c.CARD_PACK_COEF*len(self.cards))) for i in range(bigger_side_num)
        ]

        return angles_steps
