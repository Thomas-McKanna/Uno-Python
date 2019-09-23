import copy
import math
import pygame
import random
import sys

from pygame.locals import *

import cardanim.constants as c

from cardanim.util import check_for_key_press
from cardanim.shared_objects import GameObjects

from cardanim.assets import CARD_IMAGE_DICT

import cardanim.animation as animation

def main():
    # Pygame initialization and basic set up of the global variables.
    global animatables, original_surface

    pygame.init()

    clock = GameObjects.get_clock()

    pygame.display.set_caption('Uno!')

    opponents = ["Thomas", "Brendan", "Austin"]

    for name in opponents:
        animation.add_opponent(name)

    animation.init()

    i = 0
    for _ in range(2):
        for surf in CARD_IMAGE_DICT:
            animation.track_card(CARD_IMAGE_DICT[surf], i)
            i += 1
    i = 0
    primary = []
    j = 0
    opponents = []

    while True:
        check_for_key_press()

        for event in pygame.event.get():  # event handling loop
            if event.type == KEYDOWN:
                # Draw card
                if event.key == K_DOWN:
                    animation.draw_card(i)
                    primary.append(i)
                    i += 1
                # Play card
                elif event.key == K_UP:
                    animation.play_card(primary[-1])
                    primary.pop()
                    i += 1
                # Shift hand
                elif event.key == K_LEFT:
                    animation.shift_hand(False)
                elif event.key == K_RIGHT:
                    animation.shift_hand(True)
                # Opponent draw card
                elif event.key == K_0:
                    animation.opponent_draw_card("Thomas")
                    j += 1
                # Opponent play card
                elif event.key == K_1:
                    if j > 0:
                        animation.opponent_play_card("Thomas", 50 - j)

            print(event)

        animation.next_frame()
        clock.tick(c.FPS)


if __name__ == '__main__':
    main()
