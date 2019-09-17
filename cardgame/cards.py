import random
import json

class Card:
    def __init__(self, id, value: str, color: str):
        self.id = id
        self.value = value
        self.color = color
    
    def __str__(self):
        return f"{self.color} {self.value}"

    def __repr__(self):
        return str(self)

    def match(self, other):
        return self.color == other.color or self.value == other.value
    
    def reprJSON(self):
        return dict(id=self.id, value=self.value, color=self.color)

class Hand:
    def __init__(self, deck, cards=None):
        self.deck = deck
        if cards is None:
            cards = []
        if type(cards) is not list:
            raise TypeError("Cards must be a list")
        self.cards = cards
    
    def discard(self, discards):
        self.deck.discard(discards)
        self.cards = [card for card in self.cards if card not in discards]
    
    def draw(self, number):
        drawnCards = self.deck.draw(number)
        self.cards.extend(drawnCards)
        return drawnCards

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return str(self.cards)
    
    def reprJSON(self):
        return dict(deck=self.deck, cards=self.cards)
    
    def loadJSON(self, data):
        jsondata = json.loads(data)
        self.cards = jsondata["cards"]
        deckdata = json.dumps(jsondata["deck"])
        self.deck.loadJSON(deckdata)

class Deck:
    def __init__(self, discard: 'Deck' = None, cards=None):
        self.discardDeck = discard
        if cards is None:
            cards = []
        if type(cards) is not list:
            raise TypeError("Cards must be a list")
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

    def getDiscard(self):
        return self.discardDeck.cards[-1]
    
    def reprJSON(self):
        return dict(discardDeck=self.discardDeck, cards=self.cards)
    
    def loadJSON(self, data):
        jsondata = json.loads(data)
        self.cards = jsondata["cards"]
        if jsondata["discardDeck"]:
            discarddata = json.dumps(jsondata["discardDeck"])
            self.discardDeck.loadJSON(discarddata)


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj): # pylint: disable=E0202
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)
