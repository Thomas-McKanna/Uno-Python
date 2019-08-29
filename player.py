from cards import Hand, Deck
class Player: 
    def __init__(self, name, deck: Deck):
        self.name = name
        self.hand = Hand(deck)


    def draw(self, number):
        self.hand.draw(number)

    def playCard(self, idx):
        """
        Attempts to play a card from the player's hand at index idx
        """
        print(self.hand.deck.getDiscard())
        print(self.hand.cards[idx])
