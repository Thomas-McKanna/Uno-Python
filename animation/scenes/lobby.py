import pygame
import random

from ..assets import BDECK as DECK
from .. import constants as c
from ..shared_objects import SharedObjects
from ..animatable import Animatable
from ..helpers import circle_transform, put_felt_background
from ..util import show_text
from ..text_field import TextField


FORM_X = c.HALF_WINWIDTH
FORM_Y = c.WINHEIGHT * 3/4

FORM_W = c.WINWIDTH * 5/10
FORM_H = c.WINHEIGHT * 1/4

NAME_LABEL_X = c.WINWIDTH * 25/64
NAME_LABEL_Y = c.WINHEIGHT * 45/64

NAME_FIELD_X = c.WINWIDTH * 25/64
NAME_FIELD_Y = c.WINHEIGHT * 50/64
NAME_FIELD_W = c.WINWIDTH * 12/64

JOIN_BUTTON_X = c.WINWIDTH * 41/64
JOIN_BUTTON_Y = c.WINHEIGHT * 45/64
JOIN_BUTTON_W = c.WINWIDTH * 9/64

CANCEL_BUTTON_X = c.WINWIDTH * 41/64
CANCEL_BUTTON_Y = c.WINHEIGHT * 50/64
CANCEL_BUTTON_W = c.WINWIDTH * 9/64

name_field = None
join_button = None
cancel_button = None


def append_char_to_name(char):
    """
    Adds a character to the name field on the screen.
    Parameters:
    -----------
    char: the character to append (string)
    """
    # Always allow backspace
    if char == '\b':
        name_field.append_char(char)
    # Check if characters will fit in text box
    elif len(name_field.get_text()) < 15:
        name_field.append_char(char)


def get_name():
    """
    Returns that string that is the player's name.
    """
    return name_field.get_text()


def clicked_join_game(point):
    """
    Returns true if the point intersects with the join game button.
    Parameters:
    -----------
    point: (x, y) tuple for the point
    """
    return join_button.collide(point)


def clicked_cancel(point):
    """
    Returns true if the point intersects with the cancel button.
    Parameters:
    -----------
    point: (x, y) tuple for the point
    """
    return cancel_button.collide(point)


def join_button_to_waiting():
    join_button.unfocus()
    join_button.set_text("waiting")

    show_text("Finding other players...", 5)


def show():
    """
    Transitions the screen to the lobby.
    """
    ###################################################
    # Constants for Lobby Scene
    ###################################################

    BACKGROUND_COLOR = pygame.Color("darkgreen")
    BACKGROUND_BORDER_COLOR = pygame.Color("white")

    LABEL_OFFSET = 1/8

    # Make background black (clean slate)
    base_surf = SharedObjects.get_base_surface()
    base_surf.fill(pygame.Color("black"))
    base_surf = put_felt_background(base_surf)

    # Get animatables and clear any previous items
    animatables = SharedObjects.get_animatables()
    disposable_animatables = SharedObjects.get_disposable_animatables()
    animatables.clear()
    disposable_animatables.queue.clear()

    #############################################################
    # User Name and Game ID Form
    #############################################################

    # Background of form
    border_w = c.WINHEIGHT * 0.0125  # border ratio

    surf = pygame.Surface((FORM_W, FORM_H))
    surf.fill(BACKGROUND_BORDER_COLOR)

    divider_x = surf.get_rect().w * 35/64

    inside_surf = pygame.Surface(
        (FORM_W - border_w, FORM_H - border_w))
    inside_surf.fill(BACKGROUND_COLOR)

    rect = surf.get_rect()
    surf.blit(inside_surf, (border_w/2, border_w/2))

    divider_surf = pygame.Surface((border_w/2, FORM_H))
    divider_surf.fill(BACKGROUND_BORDER_COLOR)

    surf.blit(divider_surf, (divider_x, 0))

    background = Animatable(surf, c.HALF_WINWIDTH,
                            c.WINHEIGHT * 9/8, hidden=False)

    background.move(
        new_centerx=FORM_X,
        new_centery=FORM_Y
    )

    animatables.append(background)

    # Username label
    small_font = SharedObjects.get_small_font()
    name_label = small_font.render("Enter username", True, c.LOBBY_TEXT_COLOR)
    name_label = Animatable(name_label, c.WINWIDTH * -
                            1/8, NAME_LABEL_Y, hidden=False)

    name_label.move(
        new_centerx=NAME_LABEL_X,
        new_centery=NAME_LABEL_Y
    )

    animatables.append(name_label)

    # Name field
    global name_field

    name_field = TextField(NAME_FIELD_X, NAME_FIELD_Y,
                           NAME_FIELD_W, active_color=pygame.Color("forestgreen"))
    name_field.focus()
    name_field.instant_move(c.WINWIDTH * -1/8, NAME_FIELD_Y)
    name_field.move(NAME_FIELD_X, NAME_FIELD_Y)

    animatables.append(name_field)

    # Join game button
    global join_button

    # Using a text field for buttons because they provide similar functionality
    join_button = TextField(JOIN_BUTTON_X, JOIN_BUTTON_Y, JOIN_BUTTON_W,
                            active_color=c.LOBBY_JOIN_GAME_BACKGROUND_COLOR,
                            inactive_color=c.LOBBY_WAITING_BACKGROUND_COLOR, placeholder="Join Game!")
    join_button.focus()
    join_button.instant_move(c.WINWIDTH * 9/8, JOIN_BUTTON_Y)
    join_button.move(JOIN_BUTTON_X, JOIN_BUTTON_Y)

    animatables.append(join_button)

    # Cancel from lobby button
    global cancel_button

    # Using a text field for buttons because they provide similar functionality
    cancel_button = TextField(
        CANCEL_BUTTON_X, CANCEL_BUTTON_Y, CANCEL_BUTTON_W, inactive_color=c.LOBBY_CANCEL_GAME_BACKGROUND_COLOR, placeholder="Cancel")
    cancel_button.instant_move(c.WINWIDTH * 9/8, CANCEL_BUTTON_Y)
    cancel_button.move(CANCEL_BUTTON_X, CANCEL_BUTTON_Y)

    animatables.append(cancel_button)

    #############################################################
    # Additional animations
    #############################################################

    cards = []
    center_x = c.HALF_WINWIDTH
    center_y = c.WINHEIGHT * 1/3

    num_cards_per_side = 10

    #################################################
    # Creation and initialize movement inwards
    #################################################
    for i in range(num_cards_per_side):
        for x in [-1/8, 9/8]:
            card = Animatable(DECK, c.WINWIDTH * x, 0,
                              hidden=False, chain_movements=True)

            card.instant_scale(c.DEFAULT_CARD_SCALE)
            card.move(center_x, center_y, (i + 1) / 8)
            card.freeze((num_cards_per_side - i + 1) / 8)

            cards.append(card)

    ################################################
    # Infinity shape
    ################################################
    infinity_iterations = 6  # 6 works well
    infinity_step = c.WINWIDTH * 1/50
    infinity_duration = 1

    ininity_anim_sleep_dur = 0.05

    times = []
    for i, card in enumerate(cards):
        time = i * ininity_anim_sleep_dur
        times.append(time)
        card.freeze(i * ininity_anim_sleep_dur)

    for i in range(infinity_iterations):
        for j, card in enumerate(cards):
            # Left
            if i % 2 == 0:
                card.circle(center_x - (i * infinity_step), center_y,
                            360, infinity_duration + i * 1/100)
            # Right
            else:
                card.circle(center_x + (i * infinity_step), center_y, -
                            360, infinity_duration + i * 1/100)

    for i in range(infinity_iterations)[::-1]:
        for j, card in enumerate(cards):
            # Left
            if i % 2 == 0:
                card.circle(center_x - (i * infinity_step), center_y,
                            360, infinity_duration + i * 1/100)
            # Right
            else:
                card.circle(center_x + (i * infinity_step), center_y, -
                            360, infinity_duration + i * 1/100)

    #################################################
    # Increasing circles
    #################################################
    icircle_iterations = 6   # 6 works well
    icircle_step = c.WINWIDTH * 1/50
    icircle_duration = 1
    icircle_anim_sleep_dur = 0.05

    for i in range(icircle_iterations):
        for j, card in enumerate(cards):
            card.circle(center_x - (i * icircle_step), center_y,
                        360, icircle_duration + i * 1/100)

    for i in range(icircle_iterations):
        for j, card in enumerate(cards):
            card.circle(center_x + (i * icircle_step), center_y,
                        360, icircle_duration + i * 1/100)

    #################################################
    # Random location
    #################################################
    rlocation_iterations = 10
    for i in range(rlocation_iterations):
        rx = random.randint(c.WINWIDTH * 1/4, c.WINWIDTH * 3/4)
        ry = random.randint(0, c.HALF_WINHEIGHT)
        for card in cards:
            card.move(rx, ry, 1)

    for card in cards:
        card.move(center_x, center_y)

    ################################################
    # Four corners
    ################################################
    fc_iterations = 3
    fc_duration = 2

    fc_positions = [
        (c.WINWIDTH * 1/4, c.HALF_WINHEIGHT * 1/4),
        (c.WINWIDTH * 3/4, c.HALF_WINHEIGHT * 1/4),
        (c.WINWIDTH * 3/4, c.HALF_WINHEIGHT),
        (c.WINWIDTH * 1/4, c.HALF_WINHEIGHT),
    ]

    for i in range(fc_iterations)[::-1]:
        dur = random.random() * 2
        for card in cards:
            for x, y in fc_positions:
                card.move(x, y, dur)

    for card in cards:
        card.move(center_x, center_y)

    #################################################
    # Spiral
    #################################################
    spoints = 10
    sradius = c.WINHEIGHT * 1/5

    slocations = [
        circle_transform(c.HALF_WINWIDTH, sradius,
                         center_x, center_y, 360 * ((i + 1) / spoints)) for i in range(spoints)
    ]

    for x, y in slocations:
        for card in cards:
            card.circle(x, y, 360, 1)

    #################################################
    # Vortex
    #################################################
    vinterations = 10
    vstart_radius = c.WINHEIGHT * 1/8

    vx_positions = [
        vstart_radius + (center_y - vstart_radius) * (i/vinterations) for i in range(vinterations)
    ]

    for card in cards:
        card.move(c.HALF_WINWIDTH, vstart_radius)

    for i, x in enumerate(vx_positions):
        for card in cards:
            card.move(c.HALF_WINWIDTH, x, 0.04)
            card.circle(center_x, center_y, 360, 1.5)

    for card in cards:
        card.move(center_x, center_y)

    # #################################################
    # Random shuffle
    # #################################################
    random_shuffle_iterations = 100
    for card in cards:
        for i in range(random_shuffle_iterations):
            card.move(random.randint(c.WINWIDTH * 1/4, c.WINWIDTH * 3/4),
                      random.randint(0, c.HALF_WINHEIGHT), random.randint(1, 3))
            card.freeze(random.randint(1, 3))
            card.move(center_x, center_y, random.randint(1, 3))

    for i, card in enumerate(cards):
        card.freeze(times.pop())

    animatables = SharedObjects.get_animatables()

    cards.reverse()
    for card in cards:
        animatables.append(card)
