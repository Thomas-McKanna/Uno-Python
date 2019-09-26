import copy
import math
import pygame
import random
import sys

import pygame.locals as pg

from cardanim.assets import CARD_IMAGE_DICT

import cardanim.animation as animation


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
            if event.type == pg.KEYDOWN:
                # Draw card
                if event.key == pg.K_DOWN:
                    animation.draw_card(i)
                    primary.append(i)
                    i += 1
                # Play card
                elif event.key == pg.K_UP:
                    animation.play_card(primary[-1])
                    primary.pop()
                    i += 1
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
