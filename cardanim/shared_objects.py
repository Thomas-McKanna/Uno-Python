import copy
import pygame

class SharedObjects:
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
    font = None

    @staticmethod
    def get_clock():
        """
        Returns a pygame.time.Clock object.
        """
        if SharedObjects.fps_clock is None:
            SharedObjects.fps_clock = pygame.time.Clock()
        return SharedObjects.fps_clock

    @staticmethod
    def get_surface():
        """
        Returns the primary pygame Surface upon which all other surfaces are
        drawn.
        """
        if SharedObjects.display_surf is None:
            SharedObjects.display_surf = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
            # SharedObjects.display_surf = pygame.display.set_mode(
            #     (c.WINWIDTH, c.WINHEIGHT))
            SharedObjects.base_surf = SharedObjects.display_surf.copy()
        return SharedObjects.display_surf

    @staticmethod
    def get_base_surface():
        """
        Returns the a copy of the primary game Surface on which all other
        surfaces are drawn. Different from get_surface in that the Surface
        returned by get_surface may already have things drawn on it.
        """
        if SharedObjects.base_surf is None:
            SharedObjects.get_surface()
        return SharedObjects.base_surf

    @staticmethod
    def get_animatables():
        """
        Returns a list of animatable objects. Every object in this list will be
        redraw on every frame according to its get_frame method. If you wish
        for something to stop being animated, you must remove it from this
        list.
        """
        if SharedObjects.animatables is None:
            SharedObjects.animatables = []
        return SharedObjects.animatables
        
    @staticmethod
    def get_font():
        """
        Returns a pygame Font object which can be used to render text.
        """
        if SharedObjects.font is None:
            SharedObjects.font = pygame.font.Font(
                "cardanim/assets/Acme-Regular.ttf", round(0.04*SharedObjects.get_surface().get_rect().w))
        return SharedObjects.font