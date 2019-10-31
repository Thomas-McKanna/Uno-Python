import pygame

from .animatable import Animatable
from .shared_objects import SharedObjects

from . import constants as c


class TextField(Animatable):
    def __init__(self, x, y, width, text_color=c.LOBBY_TEXT_COLOR, active_color=c.LOBBY_ACTIVE_COLOR, inactive_color=c.LOBBY_INACTIVE_COLOR,  placeholder=None):
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
        self.font = SharedObjects.get_small_font()
        self.width = width
        self.height = self.font.render(
            "I", True, text_color).get_rect().h
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.is_active = False
        self.text_color = text_color

        if placeholder is not None:
            self.text = placeholder
        else:
            self.text = ""

        surf = self._make_surface()

        super(TextField, self).__init__(surf, x, y, hidden=False)

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

        text_surf = self.font.render(self.text, True, self.text_color)
        rect = text_surf.get_rect()
        rect.center = center

        background_surf.blit(text_surf, rect)

        return background_surf

    def _update_animatable(self):
        surf = self._make_surface()

        self.original_surface = surf
        self.surface = surf

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

    def set_text(self, txt):
        """
        Immediately changes the text to the passed in string.
        Parameters:
        -----------
        txt: string
        """
        self.text = txt
        self._update_animatable()

    def collide(self, point):
        """
        Returns true if the point is within the text field.
        Parameters:
        -----------
        point: (x, y) tuple of the point
        """
        rect = self.rect
        return rect.collidepoint(point)
