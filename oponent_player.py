from player import Player
from spread_deck import SimpleSpreadDeck
from assets import DECK

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

        self.spread_deck = SimpleSpreadDeck(
            self.spread_x, 
            self.spread_y, 
            self.spread, 
            c.OPPONENT_SPREAD_DECK_CARD_SCALE,
            DECK
        )

    def animate_draw_card(self):
        """
        Draws a card from the draw deck and adds it to the spread deck. The
        card is not revealed on the screen.
        """
        self.spread_deck.add_card()