import pytest
from cardgame.cards import Card, Hand, Deck, ComplexEncoder




# Test Card class

def test_card_str():
    card = Card(1, "4", "Red")
    assert card.__str__() == "Red 4"

def test_card_repr():
    card = Card(1, "4", "Red")
    assert card.__repr__() == "Red 4"

@pytest.mark.parametrize("card1, card2, output",
[(Card(1, "4", "Red"), Card(2, "4", "Blue"), True), # Test value match
 (Card(1, "5", "Red"), Card(2, "4", "Red"), True),  # Test color match
 (Card(1, "2", "Red"), Card(2, "4", "Blue"), False), # Test no match
 (Card(1, "4", "Red"), Card(2, "4", "Red"), True)] # Test both match
)
def test_card_match(card1, card2, output):
    assert card1.match(card2) == output

def test_card_reprJSON():
    output = {"id": 1, "value": "4", "color": "Red"}
    card = Card(1, "4", "Red")
    assert card.reprJSON() == output

# Test Deck class
@pytest.fixture
def test_deck_setup():
    discardDeck = Deck(None, None)
    cards = []
    colors = ["Red", "Green", "Yellow", "Blue"]
    for color in colors:
        cards.append(Card(len(cards), str(0), color))
        for num in range(1,10):
            cards.append(Card(len(cards), str(num), color))
        cards.append(Card(len(cards), "+2", color))
        cards.append(Card(len(cards), "skip", color))
        cards.append(Card(len(cards), "reverse", color))
    cards.append(Card(len(cards), "wild", "wild"))
    cards.append(Card(len(cards), "+4", "wild"))

    deck = Deck(discardDeck, cards)
    return deck

def test_empty_deck():
    deck = Deck()
    assert deck.discardDeck == None
    assert deck.cards == []

def test_deck_no_discard():
    sample_card = Card(1, "4", "Red")
    deck = Deck(None, [sample_card])
    assert deck.cards[0] == sample_card

def test_deck():
    sample_discard = Deck()
    sample_card = Card(1, "4", "Red")
    deck = Deck(sample_discard, [sample_card])
    assert deck.cards[0] == sample_card
    assert deck.discardDeck == sample_discard

def test_deck_not_list():
    sample_card = Card(1, "4", "Red")
    with pytest.raises(TypeError):
        deck = Deck(None, sample_card)

def test_deck_draw(test_deck_setup):
    drawncard = test_deck_setup.draw(1)
    assert str(drawncard[0]) == str(Card(1, "+4", "wild"))

def test_deck_draw_excess_reshuffle():
    discardDeck = Deck(None, [Card(1, "3", "Red"), Card(2, "4", "Blue")])
    cards = [Card(3, "5", "Yellow"), Card(4, "6", "Green")]
    deck = Deck(discardDeck, cards)
    drawn_cards = deck.draw(3)
    assert len(drawn_cards) == 3

def test_deck_draw_excess_no_discard():
    cards = [Card(3, "5", "Yellow"), Card(4, "6", "Green")]
    deck = Deck(None, cards)
    drawn_cards = deck.draw(3)
    assert len(drawn_cards) == 2

def test_deck_shuffle(test_deck_setup):
    # This test may fail due to random chance if the first
    # cards happen to be unchanged after the shuffle
    old5cards = test_deck_setup.cards[:5]
    test_deck_setup.shuffle()
    new5cards = test_deck_setup.cards[:5]
    assert old5cards != new5cards

def test_deck_discard(test_deck_setup):
    topcard = test_deck_setup.cards[-1]
    test_deck_setup.discard(test_deck_setup.draw(1))
    removal = topcard not in test_deck_setup.cards
    discard = topcard == test_deck_setup.discardDeck.cards[-1]
    assert removal
    assert discard


def test_deck_getDiscard():
    discardDeck = Deck(None, [Card(1, "3", "Red"), Card(2, "4", "Blue")])
    cards = [Card(3, "5", "Yellow"), Card(4, "6", "Green")]
    deck = Deck(discardDeck, cards)

    assert str(deck.getDiscard()) == "Blue 4"

def test_deck_getDiscard_empty():
    discardDeck = Deck()
    cards = [Card(3, "5", "Yellow"), Card(4, "6", "Green")]
    deck = Deck(discardDeck, cards)

    assert deck.getDiscard() == None

def test_deck_reprJSON():
    discardDeck = Deck(None, [Card(1, "3", "Red"), Card(2, "4", "Blue")])
    cards = [Card(3, "5", "Yellow"), Card(4, "6", "Green")]
    deck = Deck(discardDeck, cards)
    assert deck.reprJSON() == dict(discardDeck = deck.discardDeck, cards = deck.cards)

def test_deck_loadJSON():
    testjson = """
{"discardDeck": {"discardDeck": null, "cards": [{"id": 101, "value": "wild", "color": "wild"}]}, "cards":
[{"id": 54, "value": "2", "color": "Yellow"}, {"id": 28, "value": "2", "color": "Green"}, {"id": 15, "value": "8", "color": "Red"}, {"id": 77, "value": "1", "color": "Blue"}, {"id": 99, "value": "reverse", "color": "Blue"}]}
"""
    deck = Deck()
    deck.loadJSON(testjson)
    assert len(deck.cards) == 5
    assert len(deck.discardDeck.cards) == 1
    assert deck.discardDeck.discardDeck is None


'''
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
'''