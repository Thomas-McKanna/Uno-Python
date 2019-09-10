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
HAND_CIRCLE_CENTER_Y = 4 * WINHEIGHT // 2

# X-position where the focus card it located
FOCUS_CARD_X = WINWIDTH // 2

# Y-position where the focus card it located
FOCUS_CARD_Y = 5 * WINHEIGHT // 6

# Size of focused card compared to original asset size
FOCUS_CARD_SCALE = 0.27

# Size of cards compared to original asset size
DEFAULT_CARD_SCALE = 0.22

# How many seconds it should take for rotate hand by one card
SHIFT_HAND_DURATION = 0.15

# X-position of center of play deck (deck that players put choice on)
PLAY_DECK_CENTER_X = 5 * WINWIDTH // 8

# Y-position of center of play deck (deck that players put choice on)
PLAY_DECK_CENTER_Y = WINHEIGHT // 2

# X-position of center of draw deck (deck that players draw cards from)
DRAW_DECK_CENTER_X = 3 * WINWIDTH // 8

# Y-position of center of draw deck (deck that players draw cards from)
DRAW_DECK_CENTER_Y = WINHEIGHT // 2

# The farthest possible angle a card can be away from the focus card
HAND_BOUNDARY_ANGLE = 30

# A unit-less coefficient that effect how tightly a hand is packed together
CARD_PACK_COEF = 0.2