import random

class Deck:
    """
    Represents a deck of cards.
    """
    def __init__(self, cards=None):
        """
        cards: a list of Card objects
        """
        if cards is not None:
            self.cards = cards
        else:
            self.cards = []

    def push(self, card):
        """
        Adds a card to the top of the deck.
        Parameters:
        -----------
        card: a Card object
        """
        self.cards.append(card)

    def pop(self):
        """
        Removes the top card on the deck and returns it. If the deck is empty,
        None is returned.
        """
        if len(self.cards):
            top_card = self.cards[-1]
            self.cards = self.cards[:-1]
            return top_card
        else:
            return None

    def shuffle(self):
        """
        Randomly reorganized the deck.
        """
        random.shuffle(self.cards)
