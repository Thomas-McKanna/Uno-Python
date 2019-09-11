"""
This file contains contstant values used throughout the program.
"""

# Frames per second (how many times screen it updated in one second)
FPS = 30

# Width of the game window in pixels
WINWIDTH = 1000

# Height of the game window in pixels
WINHEIGHT = 750

# Half the width of the game window in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)

# Half the height of the game window in pixels
HALF_WINHEIGHT = int(WINHEIGHT / 2)

# X-position of imaginary circle that hand rotates around
HAND_CIRCLE_CENTER_X = WINWIDTH // 2

# Y-position of imaginary circle that hand rotates around
HAND_CIRCLE_CENTER_Y = 3 * WINHEIGHT // 2

# X-position where the focus card it located
FOCUS_CARD_X = WINWIDTH // 2

# Y-position where the focus card it located
FOCUS_CARD_Y = 5 * WINHEIGHT // 6

# Size of focused card compared to original asset size
FOCUS_CARD_SCALE = 0.325

# Size of cards compared to original asset size
DEFAULT_CARD_SCALE = 0.22

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

# The size of font rendered onto the screen
FONT_SIZE = round(0.04*WINWIDTH)

# The color of the font rendered onto the screen
from pygame import Color
FONT_COLOR = Color('white')

# How long it takes to perform the add card to player spread deck animation
OPPONENT_SPREAD_DECK_ANI_DURATION = 0.2

# Size of spread deck cards compared to original asset size
OPPONENT_SPREAD_DECK_CARD_SCALE = 0.1

# Absolute number of pixel away from the center of an opponent card spread
# the center of any card in the spread can be
OPPONENT_SPREAD_PX = 40