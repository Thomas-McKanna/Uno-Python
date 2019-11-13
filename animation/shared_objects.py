import copy
import pygame


class DisposableAnimatables:
    """
    Holds a limited sized list of animatables. Once the queue is full, new
    additions will push out the oldest element. The purpose of this class is
    to prevent a large buildup of unused and covered up animatables over the
    course of a game.
    """

    def __init__(self):
        self.queue = []

    def append(self, animatable):
        if len(self.queue) > 60:
            self.queue = self.queue[1:]
        self.queue.append(animatable)

    def remove(self, animatable):
        self.queue.remove(animatable)

    def __iter__(self):
        return self.queue.__iter__()

    def __len__(self):
        return len(self.queue)


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
    disposable_animatables = None
    small_font = None
    medium_font = None
    large_font = None
    extra_large_font = None

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
            SharedObjects.display_surf = pygame.display.set_mode(
               (0, 0), pygame.FULLSCREEN)
            # SharedObjects.display_surf = pygame.display.set_mode(
            #      (1800,1000))
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
    def get_disposable_animatables():
        """
        Returns a list of animatable objects. Every object in this list will be
        redraw on every frame according to its get_frame method. If you wish
        for something to stop being animated, you must remove it from this
        list.
        """
        if SharedObjects.disposable_animatables is None:
            SharedObjects.disposable_animatables = DisposableAnimatables()
        return SharedObjects.disposable_animatables

    @staticmethod
    def get_small_font():
        """
        Returns a pygame Font object which can be used to render text.
        """
        if SharedObjects.small_font is None:
            SharedObjects.small_font = pygame.font.Font(
                "animation/assets/Acme-Regular.ttf", round(0.04*SharedObjects.get_surface().get_rect().h))
        return SharedObjects.small_font

    @staticmethod
    def get_medium_font():
        """
        Returns a pygame Font object which can be used to render text.
        """
        if SharedObjects.medium_font is None:
            SharedObjects.medium_font = pygame.font.Font(
                "animation/assets/Acme-Regular.ttf", round(0.05*SharedObjects.get_surface().get_rect().h))
        return SharedObjects.medium_font

    @staticmethod
    def get_large_font():
        """
        Returns a pygame Font object which can be used to render text.
        """
        if SharedObjects.large_font is None:
            SharedObjects.large_font = pygame.font.Font(
                "animation/assets/Acme-Regular.ttf", round(0.06*SharedObjects.get_surface().get_rect().h))
        return SharedObjects.large_font

    @staticmethod
    def get_extra_large_font():
        """
        Returns a pygame Font object which can be used to render text.
        """
        if SharedObjects.extra_large_font is None:
            SharedObjects.extra_large_font = pygame.font.Font(
                "animation/assets/Acme-Regular.ttf", round(0.08*SharedObjects.get_surface().get_rect().h))
        return SharedObjects.extra_large_font
