from cards import Hand, Deck
class Player: 
    def __init__(self, name, deck: Deck):
        self.name = name
        self.hand = Hand(deck)


    def draw(self, number):
        return self.hand.draw(number)

    def playCard(self, idx):
        """
        Attempts to play a card from the player's hand at index idx
        """
        try:
            choice = self.hand.cards[idx]
        except IndexError:
            print("Card index out of range.")
            return False
        curDiscard = self.hand.deck.getDiscard()

        if choice.color == curDiscard.color or choice.value == curDiscard.value:
            self.hand.discard([choice])
            print(f"Player: {choice}")
            return True
        else:
            print("Card does not match color or number.")
            return False

