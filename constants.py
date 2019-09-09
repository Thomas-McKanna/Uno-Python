"""
This file contains contstant values used throughout the program.
"""

from shared_objects import GameObjects

surf = GameObjects.get_surface()

# Frames per second (how many times screen it updated in one second)
FPS = 30

# Width of the game window in pixels
WINWIDTH = surf.get_rect().w

# Height of the game window in pixels
WINHEIGHT = surf.get_rect().h

# Half the width of the game window in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)

# Half the height of the game window in pixels
HALF_WINHEIGHT = int(WINHEIGHT / 2)

# X-position of imaginary circle that hand rotates around
HAND_CIRCLE_CENTER_X = WINWIDTH // 2

# Y-position of imaginary circle that hand rotates around
HAND_CIRCLE_CENTER_Y =  3 * WINHEIGHT // 2

# X-position where the focus card it located
FOCUS_CARD_X = WINWIDTH // 2

# Y-position where the focus card it located
FOCUS_CARD_Y = 5 * WINHEIGHT // 6

# Size of focused card compared to original asset size
FOCUS_CARD_SCALE = 0.00026 * WINWIDTH

# Size of cards compared to original asset size
DEFAULT_CARD_SCALE = 0.0002 * WINWIDTH

# How many seconds it should take for rotate hand by one card
ROTATE_HAND_DURATION = 0.2

# X-position of center of play deck (deck that players put choice on)
PLAY_DECK_CENTER_X = 5 * WINWIDTH // 8

# Y-position of center of play deck (deck that players put choice on)
PLAY_DECK_CENTER_Y = WINHEIGHT // 2

# X-position of center of draw deck (deck that players draw cards from)
DRAW_DECK_CENTER_X = 3 * WINWIDTH // 8

# Y-position of center of draw deck (deck that players draw cards from)
DRAW_DECK_CENTER_Y = WINHEIGHT // 2