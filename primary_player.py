from player import Player
from primary_player_hand import PrimaryHand
from deck import Deck
from shared_objects import GameObjects


class PrimaryPlayer(Player):
    """
    Represent the player in this Uno game who is playing against opponent
    players.
    """

    def __init__(self, name):
        super(PrimaryPlayer, self).__init__(name)

        self.hand = PrimaryHand()

    def draw_card(self):
        """
        Draws a card from the draw deck and adds it to the hand. The
        card is revealed on the screen.
        Parameters:
        -----------
        deck: a Deck object containing cards to draw from
        """
        draw_deck = GameObjects.get_draw_deck()
        card = draw_deck.pop()
        if card is not None:
            self.hand.draw_card(card)

    def play_card(self):
        """
        Plays the focus card, moving it from spread deck to the play deck. The 
        card is revealed on the screen.
        """
        # Pop the card off of the spread deck (passing random, meaningless
        # card for now)
        card = self.hand.play_card()

        if card is None:
            return

        # Clean up for animatables that are made in previous calls to this
        # function
        self.add_to_last_played_cards(card)

    def shift_hand(self, right=True):
        """
        The player shifts the cards in their hand, focus on a new card to 
        potentially play.
        Parameters:
        -----------
        right: True if the next focus card should be the card to the right
            of the current focus card, and False if to the left
        """
        self.hand.shift(right)
