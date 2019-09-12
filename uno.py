import pygame

from pygame.locals import *

from shared_objects import GameObjects
from oponent_player import Opponent
from primary_player import PrimaryPlayer

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
        base_surf = GameObjects.get_base_surface()

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
    
        base_surf = GameObjects.get_base_surface()
        for i, player in enumerate(self.opponents):
            name_surface = player.get_name_surface()
            rect = name_surface.get_rect()
            x, y = positions[i]
            rect.center = (x, y)
            base_surf.blit(name_surface, rect)

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
                    elif event.key == K_LEFT:
                        self.primary_player.shift_hand(right=False)
                        wait(c.MOVE_CARD_ANI_DURATION)
                    elif event.key == K_DOWN:
                        self.primary_player.draw_card()
                        wait(c.MOVE_CARD_ANI_DURATION)
                    elif event.key == K_UP:
                        self.primary_player.play_card()
                        wait(c.MOVE_CARD_ANI_DURATION)

            pygame.display.update()
            clock.tick(c.FPS)

    def do_stuff(self):
        """
        This function is entirely for testing purposes.
        """
        keys = list(CARD_IMAGE_DICT.keys())
        random.shuffle(keys)
        temp_card = Card(
            DECK, 
            scale=c.DRAW_DECK_SCALE,
            x=c.DRAW_DECK_CENTER_X, 
            y=c.DRAW_DECK_CENTER_Y
        )
        GameObjects.get_base_surface().blit(temp_card.surface, temp_card.rect)
        while True:
            for opponent in self.opponents:
                for _ in range(5):
                    opponent.animate_draw_card()
                    wait(c.MOVE_CARD_ANI_DURATION)

            for opponent in self.opponents:
                for _ in range(5):
                    opponent.animate_play_card(
                        Card(CARD_IMAGE_DICT[keys[random.randint(0, len(keys) - 1)]]))
                    wait(c.MOVE_CARD_ANI_DURATION)
