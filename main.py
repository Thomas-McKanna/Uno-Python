from cards import *


# Generate cards for UNO
cards = []
colors = ["Red", "Green", "Yellow", "Blue"]
for color in colors:
    cards.append(Card(len(cards), str(0), color))
    for num in range(1,10): # generate 2 cards each from [1 - 9]
        cards.append(Card(len(cards), str(num), color))
        cards.append(Card(len(cards), str(num), color))
    cards.append(Card(len(cards), "+2", color))
    cards.append(Card(len(cards), "+2", color))
    cards.append(Card(len(cards), "skip", color))
    cards.append(Card(len(cards), "skip", color))
    cards.append(Card(len(cards), "reverse", color))
    cards.append(Card(len(cards), "reverse", color))
cards.append(Card(len(cards), "wild", "wild"))
cards.append(Card(len(cards), "wild", "wild"))
cards.append(Card(len(cards), "wild", "wild"))
cards.append(Card(len(cards), "wild", "wild"))
cards.append(Card(len(cards), "+4", "wild"))
cards.append(Card(len(cards), "+4", "wild"))
cards.append(Card(len(cards), "+4", "wild"))
cards.append(Card(len(cards), "+4", "wild"))

# Populate main deck and create discard
discard = Deck() 
deck = Deck(discard=discard, cards=cards)
deck.shuffle()
discard.cards = deck.draw(1) # Discard the top card of the deck

hand = Hand(deck) # Create a hand
hand.draw(7) # Initial deal
print("Hand: ", hand)
print("Discard pile: ", discard.cards)
