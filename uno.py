import random
import sys
import copy
import pygame
import math

from pygame.locals import *
from assets import CARD_IMAGE_DICT, LOGO

from card import Card
from hand import Hand
from shared_objects import GameObjects
from constants import FPS, WINWIDTH, WINHEIGHT, HAND_CIRCLE_CENTER_X, HAND_CIRCLE_CENTER_Y, DRAW_DECK_CENTER_X, DRAW_DECK_CENTER_Y, PLAY_DECK_CENTER_X, PLAY_DECK_CENTER_Y, FOCUS_CARD_SCALE
from util import checkForKeyPress

animatables = []
surface = GameObjects.get_surface()
clock = GameObjects.get_clock()
original_surface = surface.copy()


def main():
    # Pygame initialization and basic set up of the global variables.
    global animatables, original_surface

    pygame.init()

    pygame.display.set_caption('Uno!')

    # Move in the decks
    set_background()

    # Give time for the animation to complete
    wait(1)

    # Clear animatables from intro animation
    animatables = []

    # Set background to include the decks
    store_background()

    keys = list(CARD_IMAGE_DICT.keys())
    random.shuffle(keys)

    cards = [
        Card(CARD_IMAGE_DICT[random.choice(keys)], HAND_CIRCLE_CENTER_X, HAND_CIRCLE_CENTER_Y) for _ in range(14)
    ]
    for card in cards:
        animatables.append(card)

    hand = Hand(cards)

    hand.arrange()

    while True:
        draw_next_frame()

        checkForKeyPress()

        for event in pygame.event.get():  # event handling loop
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    hand.rotate(clockwise=True)
                elif event.key == K_LEFT:
                    hand.rotate(clockwise=False)

        pygame.display.update()
        clock.tick(FPS)


def set_background():
    """
    Moves all static assets onto the screen.
    """
    draw_deck = Card(
        surface=CARD_IMAGE_DICT['DECK'],
        x=DRAW_DECK_CENTER_X,
        y=-100  # start off-screen
    )
    draw_deck.instant_scale(FOCUS_CARD_SCALE)

    play_deck = Card(
        surface=CARD_IMAGE_DICT['DASH'],
        x=PLAY_DECK_CENTER_X,
        y=-100  # start off-screen
    )
    play_deck.instant_scale(FOCUS_CARD_SCALE)

    animatables.append(draw_deck)
    animatables.append(play_deck)

    draw_deck.move(DRAW_DECK_CENTER_X, DRAW_DECK_CENTER_Y, 1)
    play_deck.move(PLAY_DECK_CENTER_X, PLAY_DECK_CENTER_Y, 1)


def store_background():
    """
    Makes the current game screen the new background upon which animatables
    are drawn.
    """
    global original_surface, surface
    original_surface = surface.copy()


def wait(seconds):
    """
    Continues to update animations, but delays user interaction (other than
    to exit) for the given number of seconds.
    """
    num_frames = round(seconds / (1 / FPS))
    for _ in range(num_frames):
        draw_next_frame()
        checkForKeyPress()
        pygame.display.update()
        clock.tick(FPS)


def draw_next_frame():
    """
    Draws the next frame for each of the animatables.
    """
    # Restore background
    surface.blit(original_surface, (0, 0))

    frames = []
    for animatable in animatables:
        frames.append(animatable.get_frame())

    # Draw animatables on top of background
    surface.blits(frames)


if __name__ == '__main__':
    main()
