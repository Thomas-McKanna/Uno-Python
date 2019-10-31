import random
import pygame

from ..assets import DECK, CARDS, BLANK
from .. import constants as c
from ..shared_objects import SharedObjects
from ..animatable import Animatable
from ..helpers import put_felt_background

_start_card = None
_exit_card = None


def _set_start_card(card):
    global _start_card
    _start_card = card


def _set_exit_card(card):
    global _exit_card
    _exit_card = card


def clicked_start(point):
    """
    Checks if the point collides with the start card on the intro screen.
    Parameters:
    -----------
    point: (x, y) tuple
    """
    if _start_card is not None:
        rect = _start_card.rect
        return rect.collidepoint(point)
    else:
        return False


def clicked_exit(point):
    """
    Checks if the point collides with the exit card on the intro screen.
    Parameters:
    -----------
    point: (x, y) tuple
    """
    if _exit_card is not None:
        rect = _exit_card.rect
        return rect.collidepoint(point)
    else:
        return False


def show():
    ###################################################
    # Constants for Intro Scene
    ###################################################
    MAIN_CARD_SIZE = c.WINHEIGHT*0.0006
    SECONDARY_CARD_SIZE = c.WINHEIGHT*0.008
    CIRCLE_CARD_SIZE = c.WINHEIGHT*0.00018
    CIRCLE_CARD_HEIGHT = 1/4
    SPEED = 12
    NUM_CARDS = 60
    BORDER_CARD_SCALE = c.WINHEIGHT*0.000218
    TEXT_COLOR = pygame.Color("white")
    BACKGROUND_COLOR = pygame.Color("navyblue")
    BACKGROUND_BORDER_COLOR = pygame.Color("dodgerblue3")

    # Make background black (clean slate)
    base_surf = SharedObjects.get_base_surface()
    base_surf.fill(pygame.Color("black"))

    # Get animatables and clear any previous items
    animatables = SharedObjects.get_animatables()
    disposable_animatables = SharedObjects.get_disposable_animatables()
    animatables.clear()
    disposable_animatables.queue.clear()

    # Background border surface
    surf = pygame.Surface((c.WINWIDTH, c.WINHEIGHT * 3/4))
    surf.fill(pygame.Color("darkgreen"))
    rect = surf.get_rect()
    rect.center = (c.HALF_WINWIDTH, c.HALF_WINHEIGHT)

    base_surf.blit(surf, rect)

    # Background surface
    surf = pygame.Surface((c.WINWIDTH, c.WINHEIGHT * 3/4 * 0.95))
    surf = put_felt_background(surf)
    rect = surf.get_rect()
    rect.center = (c.HALF_WINWIDTH, c.HALF_WINHEIGHT)

    base_surf.blit(surf, rect)

    keys = list(CARDS.keys())

    card_w, card_h = CARDS[keys[0]].get_rect().size
    card_w *= BORDER_CARD_SCALE
    card_h *= BORDER_CARD_SCALE

    top_border = (
        -c.HALF_WINWIDTH * 1/8,     # start_x
        card_h / 2                  # start_y
    )

    bottom_border = (
        c.WINWIDTH * 9/8,           # start_x
        c.WINHEIGHT - card_h / 2    # start_y
    )

    for info in [top_border, bottom_border]:
        x = 0
        while x < c.WINWIDTH:
            start_x, start_y = info
            card = Animatable(CARDS[random.choice(keys)], hidden=False)
            card.instant_scale(BORDER_CARD_SCALE)
            card.instant_move(start_x, start_y)
            # base.blit(card.surface, card.rect)
            card.move(
                new_centerx=x+card_w/2,
                new_centery=start_y,
                duration=1
            )
            animatables.append(card)
            x += card_w

    # Circular card chain intro animation
    start_x = -c.WINWIDTH / 2
    for i in range(NUM_CARDS):
        card = Animatable(
            surface=CARDS[random.choice(keys)],
            hidden=False,
            chain_movements=True
        )

        card.instant_scale(CIRCLE_CARD_SIZE)

        card.instant_move(start_x - c.WINWIDTH/2,
                          c.WINHEIGHT * CIRCLE_CARD_HEIGHT)

        card.rotate(9000, 300)

        # Delays cards that are farther behind in the sequence
        for j in range(i):
            card.move(
                new_centerx=start_x - c.WINWIDTH/2 + j + 1,
                new_centery=c.WINHEIGHT * CIRCLE_CARD_HEIGHT,
                duration=SPEED/150
            )

        # This sequence of movements will happen 20 times
        for _ in range(20):
            # Move card to center from left
            card.move(
                new_centerx=c.WINWIDTH * 11/12,
                new_centery=c.WINHEIGHT * CIRCLE_CARD_HEIGHT,
                duration=SPEED,
                steady=True
            )

            # Move card down
            card.move(
                new_centerx=c.WINWIDTH * 11/12,
                new_centery=c.WINHEIGHT * 3/4,
                duration=(SPEED / 3),
                steady=True
            )

            # Move card to the left
            card.move(
                new_centerx=c.WINWIDTH * 1/12,
                new_centery=c.WINHEIGHT * 3/4,
                duration=(SPEED / 2),
                steady=True
            )

            # Move card up
            card.move(
                new_centerx=c.WINWIDTH * 1/12,
                new_centery=c.WINHEIGHT * CIRCLE_CARD_HEIGHT,
                duration=(SPEED / 3),
                steady=True
            )

            # Move card to the right
            card.move(
                new_centerx=c.HALF_WINWIDTH,
                new_centery=c.WINHEIGHT * CIRCLE_CARD_HEIGHT,
                duration=(SPEED / 4),
                steady=True
            )

            # Move off screen to right
            card.move(
                new_centerx=c.WINWIDTH * 9/8,
                new_centery=c.WINHEIGHT * CIRCLE_CARD_HEIGHT,
                duration=(SPEED / 2),
                steady=True
            )

            # Move up (out of sight)
            card.move(
                new_centerx=c.WINWIDTH * 9/8,
                new_centery=-c.WINHEIGHT * 1/8,
                duration=1,
                steady=True
            )

            # Move left (out of sight)
            card.move(
                new_centerx=-c.WINWIDTH * 1/8,
                new_centery=-c.WINHEIGHT * 1/8,
                duration=1,
                steady=True
            )

            # Move down (out of sight)
            card.move(
                new_centerx=-c.WINWIDTH * 1/8,
                new_centery=c.WINHEIGHT * CIRCLE_CARD_HEIGHT,
                duration=1,
                steady=True
            )

        animatables.append(card)

    # Zoom in on logo animation
    logo = Animatable(DECK, hidden=False)
    logo.instant_move(c.HALF_WINWIDTH, c.HALF_WINHEIGHT)
    logo.scale(0.001, MAIN_CARD_SIZE, SPEED*2)
    animatables.append(logo)

    exit_card = (
        "Exit",             # text
        -c.WINWIDTH * 1/2,  # start x
        c.HALF_WINHEIGHT,   # start y
        c.WINWIDTH * 1/4,   # end x
        c.HALF_WINHEIGHT,   # end y
        _set_exit_card   # global name
    )

    start_card = (
        "Start",            # text
        c.WINWIDTH * 3/2,   # start x
        c.HALF_WINHEIGHT,   # start y
        c.WINWIDTH * 3/4,   # end x
        c.HALF_WINHEIGHT,   # end y
        _set_start_card     # global name
    )

    # Used for the text on the cards
    medium_font = SharedObjects.get_medium_font()

    # Make the text and cards and slide them in
    for info in [exit_card, start_card]:
        string, start_x, start_y, end_x, end_y, set_name = info

        raw_txt = medium_font.render(string, True, TEXT_COLOR)
        txt = Animatable(raw_txt, hidden=False)

        # Move off of the screen
        txt.instant_move(start_x, start_y)

        # Slide in
        txt.move(
            new_centerx=end_x,
            new_centery=end_y,
            duration=1
        )

        # Similar process for the card
        card = Animatable(BLANK, hidden=False)
        card.instant_scale(MAIN_CARD_SIZE)

        card.instant_move(start_x, start_y)

        card.move(
            new_centerx=end_x,
            new_centery=end_y,
            duration=1
        )

        set_name(card)

        animatables.append(card)
        animatables.append(txt)
