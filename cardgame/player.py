from .cards import Hand,Deck
class Player: 
    def __init__(self, name, deck: Deck):
        self.name = name
        self.hand = Hand(deck)


    def draw(self, number):
        return self.hand.draw(number)

    def getCardFromID(self, id):
        try:
            choice = [card for card in self.hand.cards if card.id == id][0]
        except IndexError:
            print("Card index out of range.")
            return None
        return choice
    def getCardFromIndex(self, idx):
        try:
            choice = self.hand.cards[idx]
        except IndexError:
            print("Card index out of range.")
            return None
        return choice
        
    def playCard(self, card=None, idx=None, accept_input=True):
        """
        Attempts to play a card from the player's hand
        """

        if card is None and idx is not None:
            choice = self.getCardFromIndex(idx)
        elif card is None and idx is None:
            raise Exception
        else:
            choice = card
        curDiscard = self.hand.deck.getDiscard()
        if choice.value in ["wild", "wild_draw"]:
            colorChoice = ""
            while colorChoice not in ["Red", "Green", "Yellow", "Blue"]:
                if accept_input:
                    colorChoice = input("Which color would you like to play as? ") 
                else:
                    count = {}
                    for card in self.hand.cards:
                        count[card.color] = count.get(card.color, 0) + 1
                    colorChoice = max(count, key=lambda key: count[key])
            print("Wild played as: ", colorChoice)
            choice.color = colorChoice
        if choice.match(curDiscard):
            self.hand.discard([choice])
            print(f"Player: {choice}")
            return True
        else:
            print("Card does not match color or number.")
            return False

