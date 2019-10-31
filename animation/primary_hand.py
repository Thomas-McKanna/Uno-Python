from .card import Card
from .helpers import circle_transform
from . import constants as c
from .shared_objects import SharedObjects

import time
import random


class PrimaryHand():
    """
    The hand of the player who is playing against opponents. Implements the
    same functions as OpponentHand, but with different animations.
    """

    def __init__(self):
        self.cards = []

        self.focus_index = len(self.cards) // 2

        self.last_rotate_time = time.time()

        self.angle_offset_map = {}

    def _arrange(self, scale_focus=False, move_focus=True):
        """
        Moves hand into circular position at bottom of screen.
        Parameters:
        -----------
        scale_focus: (optional) if True, focus card is scales up
            as the animation takes place
        move_focus: (optional) if True, the focus card moves to its proper
            place, otherwise it will not be moved
        """
        # If there are no cards in the hand, don't try to _arrange them
        if not len(self.cards):
            return

        # Center
        if move_focus:
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
        shift the focus card to the right or left.

        Parameters:
        -----------
        clockwise: True if rotating clockwise and False if rotating counter-
            clockwise
        Returns:
        --------
        The card that is the new focus card
        """
        if right:
            if self.focus_index + 1 == len(self.cards):
                return self.cards[self.focus_index]
            offset = 1
        else:
            if self.focus_index - 1 == -1:
                return self.cards[self.focus_index]
            offset = -1

        self.cards[self.focus_index].scale(
            c.FOCUS_CARD_SCALE,
            c.DEFAULT_CARD_SCALE,
            c.SHIFT_HAND_DURATION
        )
        self.focus_index += offset
        self.cards[self.focus_index].scale(
            c.DEFAULT_CARD_SCALE,
            c.FOCUS_CARD_SCALE,
            c.SHIFT_HAND_DURATION
        )

        self._arrange()
        print(self.focus_index)

        return self.cards[self.focus_index]

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

    def play(self, card, random_offset=True):
        """
        Moves that card in the focus card position to the play deck and moves
        one of the remaining cards into the focus card position.
        Parameters:
        -----------
        card: a Card object which is in this Hand. The card will be removed
        from the hand.
        """
        if card not in self.cards:
            # This function should only be called with default parameter, since
            # only the focus card can be played
            raise Exception

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
            from_scale=c.FOCUS_CARD_SCALE,
            to_scale=c.PLAY_DECK_SCALE,
            duration=c.MOVE_CARD_ANI_DURATION
        )

        self.cards.remove(card)

        disposable_animatables = SharedObjects.get_disposable_animatables()
        disposable_animatables.append(card)

        animatables = SharedObjects.get_animatables()
        animatables.remove(card)

        if self.focus_index >= len(self.cards):
            self.focus_index -= 1
        self._arrange(scale_focus=True)

    def draw(self, card):
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

        self._arrange(scale_focus=False, move_focus=False)

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

        if self.focus_index != 0:
            index = SharedObjects.get_animatables().index(
                self.cards[self.focus_index - 1])
            SharedObjects.get_animatables().insert(index, card)
        else:
            SharedObjects.get_animatables().insert(0, card)
