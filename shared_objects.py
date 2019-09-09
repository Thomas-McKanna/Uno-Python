import pygame
from constants import WINHEIGHT, WINWIDTH

class GameObjects:

    fps_clock = None
    display_surf = None
        
    @staticmethod
    def get_clock():
        if GameObjects.fps_clock is None:
            GameObjects.fps_clock = pygame.time.Clock()
        return GameObjects.fps_clock

    @staticmethod
    def get_surface():
        if GameObjects.display_surf is None:
            GameObjects.display_surf = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
        return GameObjects.display_surf