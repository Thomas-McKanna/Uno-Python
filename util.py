import math
import pygame
import sys

from pygame.locals import *

from shared_objects import GameObjects

import constants as c

CLOCK = GameObjects.get_clock()

surface = GameObjects.get_surface()
base_surface = GameObjects.get_base_surface()
animatables = GameObjects.get_animatables()


def check_for_key_press():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def terminate():
    pygame.quit()
    sys.exit()


def circle_transform(point_x, point_y, center_x, center_y, angle):
    angle = math.radians(angle)
    x_origin = point_x - center_x
    y_origin = point_y - center_y
    x_prime = round(x_origin * math.cos(angle) - y_origin * math.sin(angle), 2)
    y_prime = round(y_origin * math.cos(angle) + x_origin * math.sin(angle), 2)
    return (x_prime + center_x, y_prime + center_y)


def wait(seconds):
    """
    Continues to update animations, but delays user interaction (other than
    to exit) for the given number of seconds.
    """
    num_frames = round(seconds / (1 / c.FPS))
    for _ in range(num_frames):
        draw_next_frame()
        check_for_key_press()
        pygame.display.update()
        CLOCK.tick(c.FPS)


def draw_next_frame():
    """
    Draws the next frame for each of the animatables.
    """
    # Restore background
    surface.blit(base_surface, (0, 0))

    frames = []
    for animatable in animatables:
        frames.append(animatable.get_frame())

    # Draw animatables on top of background
    surface.blits(frames)
