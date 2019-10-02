"""
This file contains constant values used throughout the program.
"""

from cardanim.shared_objects import SharedObjects


surf = SharedObjects.get_surface()

# Frames per second (animation speed)
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
HAND_CIRCLE_CENTER_Y = 4 * WINHEIGHT // 2

# X-position where the focus card it located
FOCUS_CARD_X = WINWIDTH // 2

# Y-position where the focus card it located
FOCUS_CARD_Y = 5 * WINHEIGHT // 6

# Size of focused card compared to original asset size
FOCUS_CARD_SCALE = 0.00026 * WINWIDTH

# Size of cards compared to original asset size
DEFAULT_CARD_SCALE = 0.0002 * WINWIDTH

# How many seconds it should take for rotate hand by one card
SHIFT_HAND_DURATION = 0.15

# X-position of center of play deck (deck that players put choice on)
PLAY_DECK_CENTER_X = 5 * WINWIDTH // 8

# Y-position of center of play deck (deck that players put choice on)
PLAY_DECK_CENTER_Y = WINHEIGHT // 2

# Size of play deck card compared to original asset size
PLAY_DECK_SCALE = 0.00026 * WINWIDTH

# X-position of center of draw deck (deck that players draw cards from)
DRAW_DECK_CENTER_X = 3 * WINWIDTH // 8

# Y-position of center of draw deck (deck that players draw cards from)
DRAW_DECK_CENTER_Y = WINHEIGHT // 2

# Size of card deck card compared to original asset size
DRAW_DECK_SCALE = 0.00026 * WINWIDTH

# The size of font rendered onto the screen
FONT_SIZE = round(0.04*WINWIDTH)

# The color of the font rendered onto the screen
from pygame import Color
FONT_COLOR = Color('white')

# Size of spread deck cards compared to original asset size
OPPONENT_SPREAD_DECK_CARD_SCALE = 0.00013 * WINWIDTH

# Absolute number of pixel away from the center of an opponent card spread
# the center of any card in the spread can be
OPPONENT_SPREAD_PX = 40

# Coefficient determining how stretched out the hand is (1-100)
# (High values => very stretched / Low values => very squeezed)
HAND_BOUNDARY_COEF = 16

# How many seconds it takes to move a card somewhere on the screen
MOVE_CARD_ANI_DURATION = 0.4

COLOR_INACTIVE = Color('lightskyblue3')
COLOR_ACTIVE = Color('dodgerblue2')
