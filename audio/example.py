# example.py - CS3100 - Myles Hammerschmidt
# -This file demonstrates how to trigger sound effects and music on the mixer.
# -System sleeps are only to simulate real-time delays of the game loop.
# TIP : Call pygame.init() AFTER importing the audio module for latency.
# Note: The mixer is initialized in audio.py in order to load assets.
import pygame
from audio import *

import time

#Start background music 
mixer.music.play(-1) #-1 to loop music. 0 to play oneshot.

time.sleep(2.2)

sfx_card_shuffle.play()

time.sleep(3.0)

#Simulate sounds within game loop.
while(True):
    #Draw/place 3 cards then play ding noise.
    sfx_card_draw.play()
    time.sleep(0.2)
    sfx_card_place.play()
    time.sleep(0.1)
    sfx_card_draw.play()
    time.sleep(0.2)
    sfx_card_place.play()
    time.sleep(0.1)
    sfx_card_draw.play()
    time.sleep(0.2)
    sfx_card_place.play()
    
    time.sleep(0.50)
    sfx_ding.play()
    time.sleep(0.5)

    #Draw/place 3 cards then play error noise.
    sfx_card_draw.play()
    time.sleep(0.2)
    sfx_card_place.play()
    time.sleep(0.1)
    sfx_card_draw.play()
    time.sleep(0.2)
    sfx_card_place.play()
    time.sleep(0.1)
    sfx_card_draw.play()
    time.sleep(0.2)
    sfx_card_place.play()
    
    time.sleep(0.50)
    sfx_error.play()
    time.sleep(0.5)

    #Draw/place 3 cards then play UNO noise.
    sfx_card_draw.play()
    time.sleep(0.2)
    sfx_card_place.play()
    time.sleep(0.1)
    sfx_card_draw.play()
    time.sleep(0.2)
    sfx_card_place.play()
    time.sleep(0.1)
    sfx_card_draw.play()
    time.sleep(0.2)
    sfx_card_place.play()
    
    time.sleep(0.50)
    sfx_uno.play()
    time.sleep(0.5)