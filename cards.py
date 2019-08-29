import random

class Card:
    def __init__(self, id, value: str, color: str):
        self.id = id
        self.value = value
        self.color = color
    
    def __str__(self):
        return f"{self.color} {self.value}"

    def __repr__(self):
        return str(self)

class Hand:
    def __init__(self, deck, cards=None):
        self.deck = deck
        if cards is None:
            cards = []
        self.cards = cards
    
    def discard(self, discards):
        self.deck.discard(discards)
        self.cards = [card for card in self.cards if card not in discards]
    
    def draw(self, number):
        self.cards.extend(self.deck.draw(number))

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return str(self.cards)

class Deck:
    def __init__(self, discard: 'Deck' = None, cards=None):
        self.discardDeck = discard
        if cards is None:
            cards = []
        self.cards = cards

    def draw(self, number: int):
        """
        This will draw up to <number> cards. If the deck runs out of cards,
        it will add all but the top card from the discard to the deck, shuffle, 
        then continue drawing. If there is no discard deck, it will stop drawing
        cards and return what has already been drawn.
        """
        drawnCards = []
        for _ in range(number):
            if len(self.cards) == 0:
                if self.discardDeck is None or len(self.discardDeck) == 1:
                    return drawnCards
                self.cards = self.discardDeck.cards[:-1]
                self.discardDeck.cards = self.discardDeck.cards[-1:]
                self.shuffle()
            drawnCards.append(self.cards.pop())
        return drawnCards
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def discard(self, discardCards):
        self.discardDeck.cards.extend(discardCards)

    def __len__(self):
        return len(self.cards)