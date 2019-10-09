import math
import pygame

from .shared_objects import SharedObjects

from . import constants as c

surface = SharedObjects.get_surface()
base_surface = SharedObjects.get_base_surface()
animatables = SharedObjects.get_animatables()
disposable_animatables = SharedObjects.get_disposable_animatables()
clock = SharedObjects.get_clock()

def circle_transform(point_x, point_y, center_x, center_y, angle):
    angle = math.radians(angle)
    x_origin = point_x - center_x
    y_origin = point_y - center_y
    x_prime = round(x_origin * math.cos(angle) - y_origin * math.sin(angle), 2)
    y_prime = round(y_origin * math.cos(angle) + x_origin * math.sin(angle), 2)
    return (x_prime + center_x, y_prime + center_y)


def next_frame():
    """
    Draws the next frame in the game. Should be called continuously at every
    framerate interval.
    """
    global clock, surface, base_surface, animatables, disposable_animatables

    # Restore background
    surface.blit(base_surface, (0, 0))

    frames = []
    for animatable in animatables:
        potential_frame = animatable.get_frame()
        if potential_frame is not None:
            frames.append(potential_frame)

    for animatable in disposable_animatables:
        potential_frame = animatable.get_frame()
        if potential_frame is not None:
            frames.append(potential_frame)

    # Draw animatables on top of background
    surface.blits(frames)

    pygame.display.update()
    clock.tick(c.FPS)

def bring_to_front(animatable):
    """
    Brings the pass in animatable to the top of the list so that it is drawn
    on top of everthing else.
    """
    SharedObjects.get_animatables().remove(animatable)
    SharedObjects.get_animatables().append(animatable)