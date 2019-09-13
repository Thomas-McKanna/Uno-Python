import pygame

from pygame.locals import *

from shared_objects import GameObjects
from oponent_player import Opponent
from primary_player import PrimaryPlayer
from animatable import Animatable

import constants as c

# Following import just for testing purposes
from util import wait, draw_next_frame, check_for_key_press
from assets import CARD_IMAGE_DICT, DECK
import random
from card import Card


class Uno:
    """
    Represents an instance of an Uno game.
    """

    def __init__(self, draw_deck):
        """
        draw_deck: a deck of cards containing all the playable cards in this
        Uno game.
        """
        self.draw_deck = draw_deck
        self.opponents = []
        self.primary_player = None
        self.background = Animatable(
            surface=GameObjects.get_base_surface(), 
            centerx=c.HALF_WINWIDTH, 
            centery=c.HALF_WINHEIGHT, 
            hidden=False
        )

    def add_opponent(self, name):
        """
        Adds an opponent to the Uno game. Should be called before init_screen
        and start_game.
        Parameters:
        -----------
        opponent: an Opponent object
        """
        # Will be initialized later
        self.opponents.append(name)

    def set_primary_player(self, player):
        """
        Sets the primary player for this Uno game. Should be called before 
        init_screen and start_game.
        Parameters:
        -----------
        player: an PrimaryPlayer object
        """
        self.primary_player = player

    def init_game(self):
        """
        Draws the base background for this Uno game and initialized objects. 
        Requires all players in the game to be set to work correctly. Should be 
        called before start_game.
        """
        animatables = GameObjects.get_animatables()
        self.background.instant_color(pygame.Color('darkgreen'))

        animatables.append(self.background)

        draw_deck_card = Card(
            DECK,
            scale=c.DRAW_DECK_SCALE,
            x=c.DRAW_DECK_CENTER_X,
            y=c.DRAW_DECK_CENTER_Y
        )

        animatables.append(draw_deck_card)

        # Initialize and draw opponent objects

        names = self.opponents

        positions = [
            (
                (i+1)/(len(self.opponents)+1)*c.WINWIDTH,  # x-pos
                (1/10)*c.WINHEIGHT  # y-pos
            ) for i in range(len(names))
        ]

        self.opponents = [
            Opponent(
                names[i],                               # name
                positions[i][0],                        # spread_x
                positions[i][1] + 0.125*c.WINHEIGHT,    # spread_y (offset)
                c.OPPONENT_SPREAD_PX                    # spread_px
            ) for i in range(len(positions))
        ]

        for i, player in enumerate(self.opponents):
            name_surface = player.get_name_surface()
            x, y = positions[i]
            opponent_animatable = Animatable(name_surface, x, y, False)
            animatables.append(opponent_animatable)

        # Initialize the primary player object
        self.primary_player = PrimaryPlayer(self.primary_player)

        # Initialize the decks

        keys = list(CARD_IMAGE_DICT.keys())
        random.shuffle(keys)

        cards = [
            Card(CARD_IMAGE_DICT[keys[i]]) for i in range(len(keys))
        ]

        draw_deck = GameObjects.get_draw_deck()

        for card in cards:
            draw_deck.push(card)

        # REMOVE IN FUTURE
        # self.do_stuff()

    def start_game(self):
        clock = GameObjects.get_clock()
        while True:
            draw_next_frame()

            check_for_key_press()

            for event in pygame.event.get():  # event handling loop
                print(event)
                if event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        self.primary_player.shift_hand(right=True)
                        wait(c.MOVE_CARD_ANI_DURATION)
                        self.other_turns()
                    elif event.key == K_LEFT:
                        self.primary_player.shift_hand(right=False)
                        wait(c.MOVE_CARD_ANI_DURATION)
                        self.other_turns()
                    elif event.key == K_DOWN:
                        self.primary_player.draw_card()
                        wait(c.MOVE_CARD_ANI_DURATION)
                        self.other_turns()
                    elif event.key == K_UP:
                        color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256), 255)
                        self.primary_player.play_card()
                        self.background.fade_to_color(color, 3)
                        wait(c.MOVE_CARD_ANI_DURATION)
                        self.other_turns()

            pygame.display.update()
            clock.tick(c.FPS)

    def other_turns(self):
        """
        This function is entirely for testing purposes.
        """
        keys = list(CARD_IMAGE_DICT.keys())
        random.shuffle(keys)

        for opponent in self.opponents:
            rand_val = random.random()
            if rand_val < 0.5:
                opponent.draw_card()
            else:
                opponent.play_card()
            wait(c.MOVE_CARD_ANI_DURATION)
