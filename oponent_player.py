from player import Player
from opponent_hand import OpponentHand
from assets import DECK
from shared_objects import GameObjects
from util import wait

import constants as c


class Opponent(Player):
    """
    Represents an opponent player (as opposed to the primary player)
    """

    def __init__(self, name, spread_x, spread_y, spread_px):
        """
        Paramters:
        ----------
        name: the name of this player
        spread_x: x-position of the center of the spread deck
        spread_y: y-position of the cetner of the spread deck
        spread_px: number of pixel horizontally from center of spread deck
            which is the maximum the center of any card in the spread deck can
            be
        """
        super(Opponent, self).__init__(name)
        self.spread_x = spread_x
        self.spread_y = spread_y
        self.spread = spread_px

        self.hand = OpponentHand(
            self.spread_x,
            self.spread_y,
            self.spread,
            c.OPPONENT_SPREAD_DECK_CARD_SCALE,
            DECK
        )

    def draw_card(self):
        """
        Draws a card from the draw deck and adds it to the spread deck. The
        card is not revealed on the screen.
        """
        card = GameObjects.get_draw_deck().pop()
        if card is not None:
            self.hand.draw_card(card)

    def play_card(self):
        """
        Plays a card, moving it from spread deck to the play deck. The card
        is revealed on the screen.
        """
        # For now, just playing last card in hand (default behavior)
        card = self.hand.play_card()

        if card is None:
            return

        # Clean up for animatables that are made in previous calls to this
        # function
        self.add_to_last_played_cards(card)
