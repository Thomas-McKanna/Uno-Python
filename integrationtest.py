import copy
import math
import pygame
import random
import sys
import json
import pygame.locals as pg

from cardgame.cards import Card, Deck, Hand, ComplexEncoder
from cardgame.player import Player

from cardanim.assets import CARDS
import cardanim.animation as animation

def generate_uno_deck():
    # Generate cards for UNO
    cards = []
    colors = ["Red", "Green", "Yellow", "Blue"]
    for color in colors:
        cards.append(Card(len(cards), str(0), color))
        for num in range(1,10): # generate 2 cards each from [1 - 9]
            cards.append(Card(len(cards), str(num), color))
            cards.append(Card(len(cards), str(num), color))
        cards.append(Card(len(cards), "draw", color))
        cards.append(Card(len(cards), "draw", color))
        cards.append(Card(len(cards), "skip", color))
        cards.append(Card(len(cards), "skip", color))
        cards.append(Card(len(cards), "reverse", color))
        cards.append(Card(len(cards), "reverse", color))
    cards.append(Card(len(cards), "wild", "wild"))
    cards.append(Card(len(cards), "wild", "wild"))
    cards.append(Card(len(cards), "wild", "wild"))
    cards.append(Card(len(cards), "wild", "wild"))
    cards.append(Card(len(cards), "wild_draw", "wild"))
    cards.append(Card(len(cards), "wild_draw", "wild"))
    cards.append(Card(len(cards), "wild_draw", "wild"))
    cards.append(Card(len(cards), "wild_draw", "wild"))
    for card in cards:
        surface = f"{card.color.upper()}_{card.value.upper()}"
        print(surface)
        animation.track_card(CARDS[surface], card.id)

    # Populate main deck and create discard
    discard = Deck() 
    deck = Deck(discard=discard, cards=cards)
    deck.shuffle()
    discard.cards = deck.draw(1) # Discard the top card of the deck

    return deck

def check_for_key_press():
    if len(pygame.event.get(pg.QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(pg.KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == pg.K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def terminate():
    pygame.quit()
    sys.exit()


def main():
    pygame.init()
    deck = generate_uno_deck()

    pygame.display.set_caption('Uno!')

    opponent_names = ["Thomas", "Brendan", "Austin"]
    opponents = [Player(name, deck) for name in opponent_names]
    current_player = Player("Player Uno", deck)

    for opponent in opponents:
        
        animation.add_opponent(opponent.name)

    animation.init()

    i = 0
    j = 0
    opponents = []

    while True:
        check_for_key_press()

        for event in pygame.event.get():  # event handling loop
            if event.type == pg.KEYDOWN:
                # Draw card
                if event.key == pg.K_DOWN:
                    card = current_player.draw(1)[0]
                    animation.draw_card(card.id)
                # Play card
                elif event.key == pg.K_UP:
                    animation.shift_hand(False)
                    cur_card = animation.shift_hand(True)
                    current_player.playCard()
                    animation.play_card()
                # Shift hand
                elif event.key == pg.K_LEFT:
                    animation.shift_hand(False)
                elif event.key == pg.K_RIGHT:
                    animation.shift_hand(True)
                # Opponent draw card
                elif event.key == pg.K_0:
                    animation.opponent_draw_card("Thomas")
                    j += 1
                # Opponent play card
                elif event.key == pg.K_1:
                    if j > 0:
                        animation.opponent_play_card("Thomas", 50 - j)

            print(event)

        animation.next_frame()


if __name__ == '__main__':
    main()
