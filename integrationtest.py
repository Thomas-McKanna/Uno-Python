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

def reset():
    global DECK
    global CURRENT_MODE
    global CLIENT_PLAYER
    global OPPONENT_TRACKER
    global turnOrder
    global turn
    global opponents
    global playerNumToName
    global clientName
    
    networking.players = None 
    networking.playersDone = False 
    networking.PID = None        
    networking.threadStop=False  
    networking.servConnect=None
    networking.turnDir=1 
    
    DECK = None
    CURRENT_MODE = None
    CLIENT_PLAYER = None
    OPPONENT_TRACKER = None
    turnOrder=None
    turn = None
    opponents = None
    playerNumToName=None
    clientName = None
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
CLIENT_PLAYER = None
OPPONENT_TRACKER = None
turnOrder=None
turn = None
opponents = None
playerNumToName=None
clientName = None
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
            #animation.start_timer(120)
        elif networking.servConnect==0:
            searching=False
            networking.servConnect=None
            show_text("No Servers Available", 3)            
    return searching
                
def autoTurn():
    newevent = pygame.event.Event(pygame.locals.KEYDOWN, unicode="", key=274, mod=pygame.locals.KMOD_NONE) #create the event
    pygame.event.post(newevent) #add the event to the queue

def init_game():
    global DECK
    global turnOrder
    global turn
    global playerNumToName
    global opponents
    playerNumToName = {}
    DECK = generate_uno_deck()
    
    #Determine lobby leader is responsible for shuffling the deck and creating the turn order
    
    lobbyLeader=None    
    turnOrder = [] #order for game using server PIDs
    turn = None
    for playerInfo in networking.players.get("data"):        
      #print("Player Data: ", playerInfo)
      playerNumToName[playerInfo["id"]]=playerInfo["clientInfo"]["id"]
      turnOrder=turnOrder+[playerInfo["id"]] #append id to turn order
      if playerInfo["id"]==networking.PID:
        lobbyLeader=playerInfo["isLobbyLeader"] #set lobbyleader bool
      if lobbyLeader:
        turn=networking.PID #for now, lobby leader always goes first    
        
    if lobbyLeader:
      networking.turnSend(turn, turnOrder, DECK) #send the others the necessary info for the turn order and whose turn it is  
      animwait(2)
      networking.turnRec()
    else:    
      animwait(2)    
      t=networking.turnRec() #everyone else reads the data for turn info
      turn = t.get("data")["state"]["turn"]
      turnOrder = t.get("data")["state"]["order"]
      #print(t.get("data")["state"]["deck"])
      DECK.loadJSON(json.dumps(t.get("data")["state"]["deck"],cls=ComplexEncoder))

    opponent_names = networking.opponentInit() #retrieve list of opponent names
    #print("Onames: ", opponent_names)
    
    opponents = [Player(name, DECK) for name in opponent_names]

    for opponent in opponents:
        animation.game.add_opponent(opponent.name)

    global CLIENT_PLAYER
    CLIENT_PLAYER = Player(clientName, DECK)
    #print(CLIENT_PLAYER)
    animation.game.show()

    for _ in range(7):
        for i in turnOrder:
            if i==networking.PID:
                card = CLIENT_PLAYER.draw(1)[0]
                animation.game.draw_card(card.id)
            else:
                animation.game.opponent_draw_card(playerNumToName[i]);
                opponents[getPos(i)].draw(1)

    first_discard = DECK.draw(1)
    DECK.discard(first_discard)
    animation.game.draw_to_play_deck(first_discard[0].id)
    if lobbyLeader:
        show_text("Your Turn", 1)        
        animation.util.start_timer(30, autoTurn)

def endGame():
    global CURRENT_MODE
    animation.util.stop_timer()
    networking.threadStop = True    
    networking.serv.shutdown(1)
    networking.serv.close()    
    reset()
    animwait(3)
    CURRENT_MODE = Modes.INTRO
    animation.intro.show()
    animation.game.reset()
 
 
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
                clientName = animation.lobby.get_name()
                threading.Thread(target = networking.serverConnect, args = (clientName,)).start()  #start connection thread
            elif animation.lobby.clicked_cancel(position):
                print("Clicked cancel button!")
                searching=False
                endGame()
        elif event.type == pg.KEYDOWN and searching==False:
            if event.key == pg.K_7:
                animation.util.stop_timer()
            elif event.key == pg.K_8:
                def myfunc():
                    print("howdydo")
                animation.util.start_timer(3,myfunc)
            animation.lobby.append_char_to_name(chr(event.key))            
    if networking.playersDone and searching==True: #playersDone==True, so server is ready
        searching=False
        CURRENT_MODE = Modes.GAME                   
        init_game()            
    return searching


def getPos(ID):
    global turnOrder
    arr = turnOrder[:]
    arr.remove(networking.PID)
    return arr.index(ID)
    


   
def do_game_iteration():
    global CURRENT_MODE
    global turnOrder
    global turn
    global opponents
    for event in pygame.event.get():  # event handling loop
        if event.type == pg.KEYDOWN:
            # Draw card
            if event.key == pg.K_DOWN and turn == networking.PID:
                print(event)
                animation.util.stop_timer()
                sfx_card_draw.play()
                card = CLIENT_PLAYER.draw(1)[0]
                animation.game.draw_card(card.id)
				#send the draw event to the other players
                np = networking.getNextPlayer(networking.PID,turnOrder,"")
                networking.sendMove("deck",networking.PID,card.color,card.value,card.id,np)
                turn = np

            # Play card
            elif event.key == pg.K_UP and turn == networking.PID:                
                cur_card_id = animation.game.get_focus_id()
                cur_card = CLIENT_PLAYER.getCardFromID(cur_card_id)
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
                    animation.util.stop_timer()
                    CLIENT_PLAYER.playCard(cur_card)
					#send the play event to the other players
                    np = networking.getNextPlayer(networking.PID,turnOrder,cur_card.value)                    
                    networking.sendMove(networking.PID,"discard",cur_card.color,cur_card.value,cur_card.id,np)
                    turn = np
                    
                    if turn == networking.PID:
                        show_text("Your Turn", 1)
                        animation.util.start_timer(30, autoTurn)
                    if len(CLIENT_PLAYER.hand.cards) == 1:
                        sfx_uno.play()
                    elif len(CLIENT_PLAYER.hand.cards) == 0:
                        show_text("You Win!", 3)
                        networking.sendEndGame()
                        endGame()
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
                networking.threadStop = True
                CURRENT_MODE = Modes.INTRO
                animation.intro.show()
                animation.game.reset()
    #recieve networking events from other players    
    if networking.serv!=None:
      move = networking.checkMoves()
    else:
      move=None
    #only read messages from other players
    if(move != None):
      if(move.get("messageType") == "disconnect" or move.get("messageType") == "game-finished"):
        show_text("Game Over!", 3)
        endGame()
      elif(move.get("messageType") == "error"):
        raise Exception(move.get('data'))
      else: #update the clients for a game move
        if move["data"]["state"]["sender"] != networking.PID:
          if(move["data"]["state"]["source"]=="deck"):#draw
            animation.game.opponent_draw_card(playerNumToName[move["data"]["state"]["sender"]]);
            opponents[getPos(move["data"]["state"]["sender"])].draw(1)
            turn = move["data"]["state"]["nextPlayer"]
            if turn==networking.PID:
              show_text("Your Turn", 1)
              animation.util.start_timer(30, autoTurn)
          elif (move["data"]["state"]["dest"]=="discard"):#play
            wildColor=None
            if move["data"]["state"]["value"] in ["wild", "wild_draw"]:
                if move["data"]["state"]["color"]  == "Blue":
                    wildColor = 0
                elif move["data"]["state"]["color"]  == "Red":
                    wildColor = 1
                elif move["data"]["state"]["color"]  == "Yellow":
                    wildColor = 2
                else:
                    wildColor = 3                
            animation.game.opponent_play_card(playerNumToName[move["data"]["state"]["sender"]],move["data"]["state"]["cardID"],wildColor)
            opp = opponents[getPos(move["data"]["state"]["sender"])]
          
            opp.playCard(opp.getCardFromID(move["data"]["state"]["cardID"]))
            turn = move["data"]["state"]["nextPlayer"]
            
            #if turn is now this player, check if last card is draw type
            if turn==networking.PID:                
                #check if last played was draw type
                if move["data"]["state"]["value"]=="draw":
                    show_text("Draw 2!", 1)
                    np = networking.getNextPlayer(networking.PID,turnOrder,"")
                    for i in range(2):
                        sfx_card_draw.play()
                        card = CLIENT_PLAYER.draw(1)[0]
                        animation.game.draw_card(card.id)
                        #send the draw event to the other players
                        if i<1:
                            networking.sendMove("deck",networking.PID,card.color,card.value,card.id, networking.PID)
                        else:
                            networking.sendMove("deck",networking.PID,card.color,card.value,card.id, np)
                        check_for_key_press()
                        animation.next_frame()
                    turn = np
                elif move["data"]["state"]["value"]=="wild_draw":
                    show_text("Draw 4!", 1)
                    np = networking.getNextPlayer(networking.PID,turnOrder,"")
                    for i in range(4):
                        sfx_card_draw.play()
                        card = CLIENT_PLAYER.draw(1)[0]
                        animation.game.draw_card(card.id)
                        #send the draw event to the other players
                        if i<3:
                            networking.sendMove("deck",networking.PID,card.color,card.value,card.id, networking.PID)
                        else:
                            networking.sendMove("deck",networking.PID,card.color,card.value,card.id, np)
                        check_for_key_press()
                        animation.next_frame()

                    turn = np
                else:
                    show_text("Your Turn", 1)
                    animation.util.start_timer(30, autoTurn)
            
            
            
            
            
            
            
            
				
if __name__ == '__main__':
    main()
