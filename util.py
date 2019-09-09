import pygame
import sys
import math
from pygame.locals import *


def checkForKeyPress():
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
