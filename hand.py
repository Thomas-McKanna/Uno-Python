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

    def arrange(self, scale_focus=False, move_focus=True):
        """
        Moves hand into circular position at bottom of screen.
        Parameters:
        -----------
        scale_focus: (optional) if True, focus card is scales up
            as the animation takes place
        move_focus: (optional) if True, the focus card moves to its proper
            place, otherwise it will not be moved
        """
        # If there are no cards in the hand, don't try to arrange them
        if not len(self.cards):
            return

        # Center
        if move_focus:
            print(self.cards, self.focus_index)
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

    def shift(self, right=True):
        """
        Shift the focus card to the right or left.

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

    def play_focus(self):
        """
        Moves that card in the focus card position to the play deck and moves
        one of the remaining cards into the focus card position.
        Returns:
        --------
        The Card object which was played.
        """
        play_card = self.cards[self.focus_index]

        play_card.move(
            new_centerx=c.PLAY_DECK_CENTER_X,
            new_centery=c.PLAY_DECK_CENTER_Y,
            duration=c.MOVE_CARD_ANI_DURATION
        )

        play_card.scale(
            from_scale=c.FOCUS_CARD_SCALE,
            to_scale=c.PLAY_DECK_SCALE,
            duration=c.MOVE_CARD_ANI_DURATION
        )

        self.cards.remove(play_card)

        if self.focus_index >= len(self.cards):
            self.focus_index -= 1
        self.arrange(scale_focus=True)

        return play_card

    def draw_card(self, card):
        """
        Moves a cards from the draw deck to the hand, making it the new focus
        card. The card is reveals as it moves to the hand.
        Parameters:
        -----------
        card: the Card object to be added to the hand
        """
        # If there was a previously existing focus card, scale it down
        if len(self.cards):
            self.cards[self.focus_index].scale(
                from_scale=c.FOCUS_CARD_SCALE,
                to_scale=c.DEFAULT_CARD_SCALE,
                duration=c.MOVE_CARD_ANI_DURATION
            )

        # Plus one for the new card
        self.focus_index = (len(self.cards) + 1) // 2
        self.cards.insert(self.focus_index, card)

        self.arrange(scale_focus=False, move_focus=False)

        card.instant_move(c.DRAW_DECK_CENTER_X, c.DRAW_DECK_CENTER_Y)
        card.instant_scale(c.DRAW_DECK_SCALE)

        card.move(
            new_centerx=c.FOCUS_CARD_X,
            new_centery=c.FOCUS_CARD_Y,
            duration=c.MOVE_CARD_ANI_DURATION
        )

        card.scale(
            from_scale=c.DRAW_DECK_SCALE,
            to_scale=c.FOCUS_CARD_SCALE,
            duration=c.MOVE_CARD_ANI_DURATION
        )

        GameObjects.get_animatables().append(card)


