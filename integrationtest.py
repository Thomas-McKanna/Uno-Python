import copy
import math
import pygame
import random
import sys
import json
import pygame.locals as pg
import time
import enum
import networking
import threading
from cardgame.cards import Card, Deck, Hand, ComplexEncoder
from cardgame.player import Player
from animation.util import show_text
import animation

from audio.audio import *


class Modes(enum.Enum):
    INTRO = 1
    LOBBY = 2
    GAME = 3


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
    return deck


DECK = None
CURRENT_MODE = None
CURRENT_PLAYER = None
OPPONENT_TRACKER = None
turnOrder=None

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
    networking.threadStop=True
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
    global CURRENT_MODE

    pygame.init()

    pygame.display.set_caption('Uno!')

    mixer.music.play(-1)

    CURRENT_MODE = Modes.INTRO
    animation.intro.show()

    searching=False
    while True:
        check_for_key_press()
        if CURRENT_MODE == Modes.INTRO:
            searching=do_intro_iteration(searching)
        elif CURRENT_MODE == Modes.LOBBY:
            searching=do_lobby_iteration(searching)
        elif CURRENT_MODE == Modes.GAME:
            do_game_iteration()
        animation.next_frame()


def do_intro_iteration(searching):
    global CURRENT_MODE        
    for event in pygame.event.get():  # event handling loop
        if event.type == pg.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            if animation.intro.clicked_start(position):
                if searching==False:
                  searching=True
                  print("Clicked start card!")
                  show_text("Connecting to Server...", 3)
                  networking.servConnect=None
                  #networking.connect()     
                  networking.threadStop=False
                  threading.Thread(target = networking.connect).start()                        
            elif animation.intro.clicked_exit(position):
                print("Clicked exit card!")
                terminate()
        if networking.servConnect==1:  
            searching=False
            networking.servConnect=None
            CURRENT_MODE = Modes.LOBBY
            animation.lobby.show()
            animation.start_timer(120)
        elif networking.servConnect==0:
            searching=False
            networking.servConnect=None
            show_text("No Servers Available", 3)            
    return searching
                


def init_game():
    global DECK
    global turnOrder
    DECK = generate_uno_deck()
    
    #Determine lobby leader is responsible for shuffling the deck and creating the turn order
    
    lobbyLeader=None    
    turnOrder = [] #order for game using server PIDs
    turn = None
    for thing in networking.players.get("data"):            
      turnOrder=turnOrder+[thing["id"]] #append id to turn order
      if thing["id"]==networking.PID:
        lobbyLeader=thing["isLobbyLeader"] #set lobbyleader bool
      if lobbyLeader:
        turn=networking.PID #for now, lobby leader always goes first    
    
    if lobbyLeader:
      networking.turnSend(turn, turnOrder, DECK) #send the others the necessary info for the turn order and whose turn it is    
    else:    
      animwait(2)    
      t=networking.turnRec() #everyone else reads the data for turn info
      turn = t.get("data")["state"]["turn"]
      turnOrder = t.get("data")["state"]["order"]
      print(t.get("data")["state"]["deck"])
      DECK.loadJSON(json.dumps(t.get("data")["state"]["deck"],cls=ComplexEncoder))

    opponent_names = networking.opponentInit() #retrieve list of opponent names
    
    
    opponents = [Player(name, DECK) for name in opponent_names]

    for opponent in opponents:
        animation.game.add_opponent(opponent.name)

    global OPPONENT_TRACKER
    OPPONENT_TRACKER = player_cycle(opponents)

    global CURRENT_PLAYER
    CURRENT_PLAYER = Player(opponent_names[turnOrder.index(turn)], DECK)
    print(CURRENT_PLAYER)
    animation.game.show()

    for _ in range(7):
        card = CURRENT_PLAYER.draw(1)[0]
        animation.game.draw_card(card.id)
        check_for_key_press()
        animation.next_frame()

        for opponent in opponents:
            opponent.draw(1)
            animation.game.opponent_draw_card(opponent.name)
            check_for_key_press()
            animation.next_frame()

    first_discard = DECK.draw(1)
    DECK.discard(first_discard)
    animation.game.draw_to_play_deck(first_discard[0].id)


def do_lobby_iteration(searching):
    global CURRENT_MODE
    for event in pygame.event.get():  # event handling loop
        if event.type == pg.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            if animation.lobby.clicked_join_game(position) and searching==False:
                searching=True
                print("Clicked join game button!")
                animation.lobby.join_button_to_waiting()
                #animwait(10)
                threading.Thread(target = networking.serverConnect, args = (animation.lobby.get_name(),)).start()  #start connection thread
            elif animation.lobby.clicked_cancel(position):
                print("Clicked cancel button!")
                networking.threadStop=True #kill the thread that was looking for a server
                CURRENT_MODE = Modes.INTRO
                animation.intro.show()
        elif event.type == pg.KEYDOWN and searching==False:
            animation.lobby.append_char_to_name(chr(event.key))
    if networking.playersDone and searching==True: #playersDone==True, so server is ready
        searching=False
        CURRENT_MODE = Modes.GAME                   
        init_game()            
    return searching


def do_game_iteration():
    global CURRENT_MODE
    global turnOrder
    for event in pygame.event.get():  # event handling loop
        if event.type == pg.KEYDOWN:
            # Draw card
            if event.key == pg.K_DOWN:
                sfx_card_draw.play()
                card = CURRENT_PLAYER.draw(1)[0]
                animation.game.draw_card(card.id)
                opponent_turn(OPPONENT_TRACKER)
                opponent_turn(OPPONENT_TRACKER)
                opponent_turn(OPPONENT_TRACKER)

            # Play card
            elif event.key == pg.K_UP:
                cur_card_id = animation.game.get_focus_id()
                cur_card = CURRENT_PLAYER.getCardFromID(cur_card_id)
                if cur_card.match(DECK.getDiscard()):
                    sfx_card_place.play()
                    # Handle playing of wild card
                    if cur_card.value in ["wild", "wild_draw"]:
                        curr = 0
                        animation.game.show_wildcard_wheel()
                        animation.game.switch_wildcard_wheel_focus(curr)
                        enter_pressed = False
                        while not enter_pressed:
                            for event in pygame.event.get():
                                if event.type == pg.KEYDOWN:
                                    if event.key == pg.K_LEFT:
                                        curr = (curr + 1) % 4
                                    if event.key == pg.K_RIGHT:
                                        curr = (curr - 1) % 4
                                    if event.key == pg.K_RETURN:
                                        enter_pressed = True
                                    animation.game.switch_wildcard_wheel_focus(
                                        curr)
                            animation.next_frame()
                        
                        animation.game.hide_wildcard_wheel()

                        if curr == 0:
                            cur_card.color = "Blue"
                        elif curr == 1:
                            cur_card.color = "Red"
                        elif curr == 2:
                            cur_card.color = "Yellow"
                        else:
                            cur_card.color = "Green"

                        animation.game.play_card(cur_card.id, wild_color=curr)
                    else:
                        # Play non-wild card
                        animation.game.play_card(cur_card.id)

                    CURRENT_PLAYER.playCard(cur_card)
                    if len(CURRENT_PLAYER.hand.cards) == 1:
                        sfx_uno.play()
                    opponent_turn(OPPONENT_TRACKER)
                    opponent_turn(OPPONENT_TRACKER)
                    opponent_turn(OPPONENT_TRACKER)
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
                CURRENT_MODE = Modes.INTRO
                animation.intro.show()
                animation.game.reset()


if __name__ == '__main__':
    main()
