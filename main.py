import copy
import math
import pygame
import random
import sys

from pygame.locals import *

import constants as c

from assets import CARD_IMAGE_DICT, LOGO
from oponent_player import Opponent
from uno import Uno
from shared_objects import GameObjects
from util import check_for_key_press, draw_next_frame

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

    num_players = 3
    opponents = ["Thomas" for i in range(num_players)]
    
    game = Uno(None)

    for opponent in opponents:
        game.add_opponent(opponent)

    game.init_game()

    game.start_game()

    while True:
        draw_next_frame()

        check_for_key_press()

        for event in pygame.event.get():  # event handling loop
            print(event)

        pygame.display.update()
        clock.tick(c.FPS)


if __name__ == '__main__':
    main()
