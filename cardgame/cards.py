import random
import json

class Card:
    def __init__(self, id=None, value: str=None, color: str=None):
        self.id = id
        self.value = value
        self.color = color
    
    def __str__(self):
        return f"{self.color} {self.value}"

    def __repr__(self):
        return str(self)

    def match(self, other):
        return self.color == other.color or \
               self.value == other.value or \
               self.value == "wild" or \
               self.value == "wild_draw" or \
               other.color == "wild"
    
    def reprJSON(self):
        return dict(id=self.id, value=self.value, color=self.color)

    def loadJSON(self, data):
        jsondata = json.loads(data)
        self.id = jsondata["id"]
        self.value = jsondata["value"]
        self.color = jsondata["color"]
        return self
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
        

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
        cards = [Card().loadJSON(card) for card in jsondata["cards"]]
        self.cards = cards
        deckdata = json.dumps(jsondata["deck"])
        self.deck.loadJSON(deckdata)
        return self

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
        if len(self.discardDeck) == 0:
            return None
        return self.discardDeck.cards[-1]
    
    def reprJSON(self):
        return dict(discardDeck=self.discardDeck, cards=self.cards)
    
    def loadJSON(self, data):
        jsondata = json.loads(data)
        cards = [Card().loadJSON(json.dumps(card)) for card in jsondata["cards"]]
        self.cards = cards
        if jsondata["discardDeck"]:
            if self.discardDeck is None:
                self.discardDeck = Deck()
            discarddata = json.dumps(jsondata["discardDeck"])
            self.discardDeck.loadJSON(discarddata)
        return self


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj): # pylint: disable=E0202
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)
