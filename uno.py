from shared_objects import GameObjects
from oponent_player import Opponent

import constants as c

from util import wait

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
                (i+1)/(len(self.opponents)+1)*c.WINWIDTH, # x-pos
                (1/10)*c.WINHEIGHT # y-pos
            ) for i in range(len(names))
        ]

        self.opponents = [
            Opponent(
                names[i],                               # name
                positions[i][0],                        # spread_x
                positions[i][1] + 0.075*c.WINHEIGHT,    # spread_y (offset)
                c.OPPONENT_SPREAD_PX                    # spread_px
            ) for i in range(len(positions))
        ]

        for i, player in enumerate(self.opponents):
            name_surface = player.get_name_surface()
            rect = name_surface.get_rect()
            x, y = positions[i]
            rect.center = (x, y)
            base_surf.blit(name_surface, rect)

        # REMOVE IN FUTURE
        self.do_stuff()

    def start_game(self):
        pass

    def do_stuff(self):
        for opponent in self.opponents:
            for _ in range(7):
                opponent.animate_draw_card()
                wait(c.OPPONENT_SPREAD_DECK_ANI_DURATION)
