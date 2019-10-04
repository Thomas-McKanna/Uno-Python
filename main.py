import copy
import math
import pygame
import random
import sys
from cardanim.shared_objects import SharedObjects
import pygame.locals as pg

import networking

from cardanim.assets import CARDS

import cardanim.animation as animation
from audio.audio import *

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


def main():    
    # Pygame initialization and basic set up of the global variables.
    global animatables, original_surface      
    pygame.init()
    clock = SharedObjects.get_clock()
    pygame.display.set_caption('Uno!')    
    
    
    
    networking.connect(clock)
    
    lobbyLeader=None    
    turnOrder = [] #order for game using server PIDs
    turn = None
    opponentCardIds={} #opponents' hand's card IDs (just for testing)
    for thing in networking.players.get("data"):      
      if thing["id"]!=networking.PID: 
        opponentCardIds[thing["id"]]=[] #make new empty hand in the dictionary
      turnOrder=turnOrder+[thing["id"]] #append id to turn order
      if thing["id"]==networking.PID:
        lobbyLeader=thing["isLobbyLeader"] #set lobbyleader bool
      if lobbyLeader:
        turn=networking.PID #for now, lobby leader always goes first
    
    
    #print(opponentCardIds)
    
    if lobbyLeader:
      networking.turnSend(turn, turnOrder) #send the others the necessary info for the turn order and whose turn it is    
    else:      
      t=networking.turnRec() #everyone else reads the data for turn info
      turn = t.get("data")["state"]["turn"]
      turnOrder = t.get("data")["state"]["order"]
    
    #print(turn)
    #print(turnOrder)
    
    opponents = networking.opponentInit() #initialize opponent name list
    
    
    
    #print(opponents)
    
    

    for name in opponents:
        animation.add_opponent(name)

    animation.init()

    i = 0
    for _ in range(2):
        for surf in CARDS:
            animation.track_card(CARDS[surf], i)
            i += 1
    i = 0
    primary = []        
    
    
    
    
    while True:
        check_for_key_press()

        for event in pygame.event.get():  # event handling loop
            if event.type == pg.KEYDOWN:
                # Draw card
                if event.key == pg.K_DOWN:
                    if (turn==networking.PID): #can only take turn when it is your turn
                        animation.draw_card(i)
                        primary.append(i)
                        turn=networking.getNextPlayer(turn,turnOrder)
                        networking.sendMove("draw",turn) #send the other players a message saying what the move was and whose turn it is next           
                        i += 1
                # Play card
                elif event.key == pg.K_UP:
                    if (turn==networking.PID): #can only take turn when it is your turn
                        animation.play_card(primary[-1])
                        primary.pop()                  
                        turn=networking.getNextPlayer(turn,turnOrder)                        
                        networking.sendMove("play",turn) #send the other players a message saying what the move was and whose turn it is next           
                # Shift hand
                elif event.key == pg.K_LEFT: #can shift hand whenever you want though
                    animation.shift_hand(False)
                elif event.key == pg.K_RIGHT:
                    animation.shift_hand(True)                    
            print(event)       
            
        #if not turn, check for other player move
        if turn!=networking.PID: 
          res = networking.checkMoves() #result will either be None or contain info about the current player's turn
          if res!=None:
            if res["state"]["sender"]!=networking.PID: #do not read moves from yourself
              turn = res["state"]["turn"] #update turn 
              name=None
              for p in networking.players.get("data"):
                if p["id"]==res["state"]["sender"]:
                  name=p["clientInfo"]["id"] #get string name of the player who took their turn
                  break
              if name==None:
                raise exception("No player name") #this should never happen
              if res["state"]["type"]=="play": #opponent played a card
                animation.opponent_play_card(name, opponentCardIds[res["state"]["sender"]][-1])
                opponentCardIds[res["state"]["sender"]].pop()
              else:
                #opponent drew a card
                animation.opponent_draw_card(name)
                opponentCardIds[res["state"]["sender"]].append(i)
                i += 1
        animation.next_frame()


if __name__ == '__main__':
    main()                        
