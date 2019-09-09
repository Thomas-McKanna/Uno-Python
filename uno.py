import copy
import math
import pygame
import random
import sys

from pygame.locals import *

import constants as c

from assets import CARD_IMAGE_DICT, LOGO
from card import Card
from hand import Hand
from shared_objects import GameObjects
from util import check_for_key_press, draw_next_frame, terminate

animatables = []
surface = GameObjects.get_surface()
clock = GameObjects.get_clock()
original_surface = surface.copy()


def main():
    # Pygame initialization and basic set up of the global variables.
    global animatables, original_surface

    pygame.init()

    pygame.display.set_caption('Uno!')

    animatables = GameObjects.get_animatables()

    keys = list(CARD_IMAGE_DICT.keys())
    random.shuffle(keys)

    cards = [
        Card(CARD_IMAGE_DICT[random.choice(keys)], c.HAND_CIRCLE_CENTER_X, c.HAND_CIRCLE_CENTER_Y) for _ in range(14)
    ]
    for card in cards:
        animatables.append(card)

    hand = Hand(cards)

    hand.arrange()

    while True:
        draw_next_frame()

        check_for_key_press()
        for event in pygame.event.get():  # event handling loop
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    hand.rotate(clockwise=True)
                elif event.key == K_LEFT:
                    hand.rotate(clockwise=False)

        pygame.display.update()
        clock.tick(c.FPS)

    while True:
        draw_next_frame()

        check_for_key_press()

        for event in pygame.event.get():  # event handling loop
            print(event)

        pygame.display.update()
        clock.tick(c.FPS)


if __name__ == '__main__':
    main()
