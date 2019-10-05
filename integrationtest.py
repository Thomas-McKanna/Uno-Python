import copy
import math
import pygame
import random
import sys
import json
import pygame.locals as pg
import time

from cardgame.cards import Card, Deck, Hand, ComplexEncoder
from cardgame.player import Player

import animation

from audio.audio import *


def generate_uno_deck():
    # Generate cards for UNO
    cards = []
    colors = ["Red", "Green", "Yellow", "Blue"]
    for color in colors:
        cards.append(Card(len(cards), str(0), color))
        for num in range(1, 10):  # generate 2 cards each from [1 - 9]
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
        animation.game.track_card(animation.assets.CARDS[surface], card.id)

    # Populate main deck and create discard
    discard = Deck()
    deck = Deck(discard=discard, cards=cards)
    deck.shuffle()
    sfx_card_shuffle.play()
    first_discard = deck.draw(1)
    discard.cards = first_discard  # Discard the top card of the deck
    animation.game.draw_to_play_deck(first_discard[0].id)
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


def player_cycle(opponents):
    while True:
        for opponent in opponents:
            print(opponent.name)
            yield opponent


def opponent_turn(opponent_tracker):
    sleep_time = random.random() + .5
    animwait(sleep_time)
    opponent = next(opponent_tracker)
    deck = opponent.hand.deck
    matches = [card for card in opponent.hand.cards if card.match(
        deck.getDiscard())]
    if matches:
        # Play Card
        chosen_card = random.choice(matches)
        sfx_card_place.play()
        opponent.playCard(chosen_card, accept_input=False)
        animation.game.opponent_play_card(opponent.name, chosen_card.id)
        if len(opponent.hand.cards) == 1:
            sfx_uno.play()
    else:
        # Draw Card
        sfx_card_draw.play()
        opponent.draw(1)
        animation.game.opponent_draw_card(opponent.name)
    animation.next_frame()


def animwait(seconds):
    goal = pygame.time.get_ticks() + seconds*1000
    while pygame.time.get_ticks() < goal:

        animation.next_frame()
        check_for_key_press()


def main():
    pygame.init()
    deck = generate_uno_deck()

    pygame.display.set_caption('Uno!')

    opponent_names = ["Thomas", "Brendan", "Austin"]
    opponents = [Player(name, deck) for name in opponent_names]
    current_player = Player("Player Uno", deck)

    for opponent in opponents:

        animation.game.add_opponent(opponent.name)

    animation.game.show()
    opponent_tracker = player_cycle(opponents)

    for _ in range(7):
        card = current_player.draw(1)[0]
        animation.game.draw_card(card.id)
        animation.next_frame()
        # pygame.time.wait(500)

        for opponent in opponents:
            opponent.draw(1)
            animation.game.opponent_draw_card(opponent.name)
            animation.next_frame()
            # pygame.time.wait(500)

    # mixer.music.play(-1)

    # GAME START SOUND
    while True:
        check_for_key_press()
        for event in pygame.event.get():  # event handling loop
            if event.type == pg.KEYDOWN:
                # Draw card
                if event.key == pg.K_DOWN:
                    sfx_card_draw.play()
                    card = current_player.draw(1)[0]
                    animation.game.draw_card(card.id)
                    opponent_turn(opponent_tracker)
                    opponent_turn(opponent_tracker)
                    opponent_turn(opponent_tracker)

                # Play card
                elif event.key == pg.K_UP:
                    cur_card_id = animation.game.get_focus_id()
                    cur_card = current_player.getCardFromID(cur_card_id)
                    if cur_card.match(deck.getDiscard()):
                        sfx_card_place.play()
                        current_player.playCard(cur_card)
                        animation.game.play_card(cur_card.id)
                        if len(current_player.hand.cards) == 1:
                            sfx_uno.play()
                        opponent_turn(opponent_tracker)
                        opponent_turn(opponent_tracker)
                        opponent_turn(opponent_tracker)

                    else:
                        sfx_error.play()
                        print("Cannot play card")

                # Shift hand
                elif event.key == pg.K_LEFT:
                    animation.game.shift_hand(False)
                elif event.key == pg.K_RIGHT:
                    animation.game.shift_hand(True)
                # Testing wildcard wheel
                elif event.key == pg.K_9:
                    animation.game.show_wildcard_wheel()
                elif event.key == pg.K_0:
                    animation.intro.show()
                elif event.key == pg.K_1:
                    animation.game.show()

        animation.next_frame()


if __name__ == '__main__':
    main()
