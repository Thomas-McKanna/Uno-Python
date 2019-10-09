import pygame

from .. import constants as c
from ..shared_objects import SharedObjects
from ..animatable import Animatable

TEXT_COLOR = pygame.Color("white")
INACTIVE_COLOR = pygame.Color("midnightblue")
ACTIVE_COLOR = pygame.Color("dodgerblue3")
JOIN_GAME_BACKGROUND_COLOR = pygame.Color("forestgreen")
CANCEL_GAME_BACKGROUND_COLOR = pygame.Color("firebrick")

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


class TextField:
    def __init__(self, x, y, width, active_color=ACTIVE_COLOR, inactive_color=INACTIVE_COLOR,  placeholder=None):
        """
        Parameters:
        -----------
        x: center x position
        y: center y position
        width: how wide in pixels the text field
        active_color: color of background when focused
        inactive_color: color of backgorund when not focused
        placeholder: the original string that this text field has
        """
        self.x = x
        self.y = y
        self.font = SharedObjects.get_medium_font()
        self.width = width
        self.height = self.font.render(
            "I", True, TEXT_COLOR).get_rect().h
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.is_active = False

        if placeholder is not None:
            self.text = placeholder
        else:
            self.text = ""

        surf = self._make_surface()

        self.animatable = Animatable(surf, x, y, hidden=False)

    def _make_surface(self):
        """
        Internal function used to make the surface of the text field.
        """
        background_surf = pygame.Surface((self.width, self.height))

        if self.is_active:
            background_surf.fill(self.active_color)
        else:
            background_surf.fill(self.inactive_color)

        center = background_surf.get_rect().center

        text_surf = self.font.render(self.text, True, TEXT_COLOR)
        rect = text_surf.get_rect()
        rect.center = center

        background_surf.blit(text_surf, rect)

        return background_surf

    def _update_animatable(self):
        surf = self._make_surface()

        self.animatable.original_surface = surf
        self.animatable.surface = surf

    def focus(self):
        """
        The background changes to the active color.
        """
        self.is_active = True
        self._update_animatable()

    def unfocus(self):
        """
        The background changes to the inactive color.
        """
        self.is_active = False
        self._update_animatable()

    def append_char(self, char):
        """
        Sets the text of the text field.
        Parameters:
        -----------
        char: a character to append to the string (can be backspace)
        """
        if char == '\b':
            if len(self.text):
                self.text = self.text[:-1]
        else:
            self.text += char

        self._update_animatable()

    def get_text(self):
        """
        Returns the current text value of the text field.
        """
        return self.text

    def get_animatable(self):
        return self.animatable

    def collide(point):
        """
        Returns true if the point is within the text field.
        Parameters:
        -----------
        point: (x, y) tuple of the point
        """
        rect = self.animatable.rect
        return rect.collidepoint(point)


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


def show():
    """
    Transitions the screen to the lobby.
    """
    ###################################################
    # Constants for Lobby Scene
    ###################################################

    BACKGROUND_COLOR = pygame.Color("navyblue")
    BACKGROUND_BORDER_COLOR = pygame.Color("dodgerblue3")

    LABEL_OFFSET = 1/8

    # Make background black (clean slate)
    base_surf = SharedObjects.get_base_surface()
    base_surf.fill(pygame.Color("black"))

    # Get animatables and clear any previous items
    animatables = SharedObjects.get_animatables()
    disposable_animatables = SharedObjects.get_disposable_animatables()
    animatables.clear()
    disposable_animatables.queue.clear()

    #############################################################
    # User Name and Game ID Form
    #############################################################

    # Background of form
    border_w = c.WINWIDTH * 0.0125  # border ratio

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
    medium_font = SharedObjects.get_medium_font()
    name_label = medium_font.render("Enter username", True, TEXT_COLOR)
    name_label = Animatable(name_label, c.WINWIDTH * -
                            1/8, NAME_LABEL_Y, hidden=False)

    name_label.move(
        new_centerx=NAME_LABEL_X,
        new_centery=NAME_LABEL_Y
    )

    animatables.append(name_label)

    # Name field
    global name_field

    name_field = TextField(NAME_FIELD_X, NAME_FIELD_Y, NAME_FIELD_W)
    name_field.focus()
    name_field_ani = name_field.get_animatable()
    name_field_ani.instant_move(c.WINWIDTH * -1/8, NAME_FIELD_Y)
    name_field_ani.move(NAME_FIELD_X, NAME_FIELD_Y)

    animatables.append(name_field.get_animatable())

    # Join game button
    global join_button

    # Using a text field for buttons because they provide similar functionality
    join_button = TextField(JOIN_BUTTON_X, JOIN_BUTTON_Y, JOIN_BUTTON_W,
                            inactive_color=JOIN_GAME_BACKGROUND_COLOR, placeholder="Join Game!")
    join_button_ani = join_button.get_animatable()
    join_button_ani.instant_move(c.WINWIDTH * 9/8, JOIN_BUTTON_Y)
    join_button_ani.move(JOIN_BUTTON_X, JOIN_BUTTON_Y)

    animatables.append(join_button.get_animatable())

    # Cancel from lobby button
    global cancel_button

    # Using a text field for buttons because they provide similar functionality
    cancel_button = TextField(
        CANCEL_BUTTON_X, CANCEL_BUTTON_Y, CANCEL_BUTTON_W, inactive_color=CANCEL_GAME_BACKGROUND_COLOR, placeholder="Cancel")
    cancel_button_ani = cancel_button.get_animatable()
    cancel_button_ani.instant_move(c.WINWIDTH * 9/8, CANCEL_BUTTON_Y)
    cancel_button_ani.move(CANCEL_BUTTON_X, CANCEL_BUTTON_Y)

    animatables.append(cancel_button.get_animatable())

    #############################################################
    # Additional animations
    #############################################################

