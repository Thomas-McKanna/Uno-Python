import copy
import pygame

import constants as c


class GameObjects:
    """
    Class containing all objects which must be shared across multiple modules
    in the project. The idea of this is have more structure than simple making
    these values global variables. If any of the object have not yet been
    referred to, an instance will be created. All subsequent references will use
    this object.
    """

    fps_clock = None
    display_surf = None
    base_surf = None
    animatables = None

    @staticmethod
    def get_clock():
        """
        Returns a pygame.time.Clock object.
        """
        if GameObjects.fps_clock is None:
            GameObjects.fps_clock = pygame.time.Clock()
        return GameObjects.fps_clock

    @staticmethod
    def get_surface():
        """
        Returns the primary pygame Surface upon which all other surfaces are
        drawn.
        """
        if GameObjects.display_surf is None:
            GameObjects.display_surf = pygame.display.set_mode(
                (c.WINWIDTH, c.WINHEIGHT))
            GameObjects.base_surf = GameObjects.display_surf.copy()
        return GameObjects.display_surf

    @staticmethod
    def get_base_surface():
        """
        Returns the a copy of the primary game Surface on which all other
        surfaces are drawn. Different from get_surface in that the Surface
        returned by get_surface may already have things drawn on it.
        """
        if GameObjects.base_surf is None:
            GameObjects.get_surface()
        return GameObjects.display_surf

    @staticmethod
    def get_animatables():
        """
        Returns a list of animatable objects. Every object in this list will be
        redraw on every frame according to its get_frame method. If you wish
        for something to stop being animated, you must remove it from this
        list.
        """
        if GameObjects.animatables is None:
            GameObjects.animatables = []
        return GameObjects.animatables
