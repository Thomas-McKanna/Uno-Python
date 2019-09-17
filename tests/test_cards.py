import pytest
from cards import Card, Hand, Deck, ComplexEncoder




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