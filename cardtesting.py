from cards import Card, Deck, Hand, ComplexEncoder
from player import Player
import json

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

# Create 3 players
player1 = Player("Player 1", deck)
player2 = Player("Player 2", deck)
player3 = Player("Player 3", deck)
players = [player1, player2, player3]

for _ in range(7):
    for player in players:
        player.draw(1)

print(json.dumps(deck.reprJSON(), cls=ComplexEncoder))
print("\n\nNew Dict:")
testjson = """
{"discardDeck": {"discardDeck": null, "cards": [{"id": 101, "value": "wild", "color": "wild"}]}, "cards":
[{"id": 54, "value": "2", "color": "Yellow"}, {"id": 28, "value": "2", "color": "Green"}, {"id": 15, "value": "8", "color": "Red"}, {"id": 77, "value": "1", "color": "Blue"}, {"id": 99, "value": "reverse", "color": "Blue"}]}
"""
deck.loadJSON(testjson)
print(json.dumps(deck.reprJSON(), cls=ComplexEncoder))
"""
while True:
    for player in players:
        print("-------------------------------")
        print(f"{player.name}: {player.hand}")
        print(f"Discard Pile: {deck.getDiscard()}")
        action = ""
        while action not in ["play", "draw"]:
            action = input("Play/Draw: ").lower()
        if action == "play":
            while not player.playCard(idx=int(input("Which card? "))):
                pass
        elif action == "draw":
            drawnCard = player.draw(1)[0]
            print(f"Card drawn: {drawnCard}")
            if drawnCard.match(deck.getDiscard()):
                nextAction = input("Play drawn card? (y/n): ").lower()
                if nextAction == "y":
                    player.playCard(card=drawnCard)

"""