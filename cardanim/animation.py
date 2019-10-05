from . import constants as c
from .shared_objects import SharedObjects
from .opponent_hand import OpponentHand
from .primary_hand import PrimaryHand
from .assets import WILDWHEEL_RED, WILDWHEEL_BLUE, WILDWHEEL_YELLOW, WILDWHEEL_GREEN
from .assets import DECK, CARDS, BLANK
from .card import Card
from .animatable import Animatable
from pkg_resources import resource_filename
import time
import threading
import random
import pygame
import copy

# Maps id => Card
cards = {}
# Maps id => OpponentHand
opponents = {}

hand = PrimaryHand()

clock = SharedObjects.get_clock()

wildcard_quadrants = []
wildcard_background = None


def track_card(surface, id):
    """
    This function can be used to tell the animation module to start tracking a
    card, opening up several animation functions.
    Parameters:
    -----------
    surface: a pygame.Surface object
    id: a unique identifier for this card (you must keep track of this
    identifier!)
    """
    cards[id] = Card(surface)


def add_opponent(name):
    """
    Adds an opponent to visual layer of game.
    Parameters:
    -----------
    name: a string that will subsequently be used as a lookup key for
        modifying the visuals of this opponent
    """
    # Temporary value: calling init will set each opponent to a position tuple.
    opponents[name] = None


def play_card(id):
    """
    Moves the card with the given id to the play deck. This function operates
    on the primary player in the game.
    Parameters:
    -----------
    id: integer value uniquely identifying a card
    """
    card = cards[id]
    hand.play(card)


def draw_card(id):
    """
    The card with the given id moves from the draw deck into the player's hand.
    The card becomes the focus card.
    Parameters:
    -----------
    id: integer value uniquely identifying a card
    """
    card = cards[id]
    hand.draw(card)


def opponent_draw_card(opponent_id):
    """
    Moves an uno card from the draw deck to the opponent's hand.
    Parameters:
    -----------
    opponent_id: integer value uniquely identifying an opponent
    """
    opponent_hand = opponents[opponent_id]
    opponent_hand.draw()


def opponent_play_card(opponent_id, card_id):
    """
    The card is revealed and moved to the play deck.
    Parameters:
    -----------
    opponent_id: integer value uniquely identifying an opponent
    card_id: integer value uniquely identifying a card
    """
    opponent_hand = opponents[opponent_id]
    card = cards[card_id]
    opponent_hand.play(card)


def shift_hand(right=True):
    """
    Shifts the focus of the player's hand.
    Parameters:
    -----------
    right: if True, focus moves to the right. Else, moves to the left.
    Returns:
    --------
    The id of the new focus card
    """
    card = hand.shift(right)

    for cid in cards:
        if cards[cid] == card:
            return cid

    # Card should have been found
    raise Exception


def draw_to_play_deck(id):
    """
    Reveals a card on top of the draw deck and moves it to the play deck. Used
    at the beginning of game to follow conventional Uno rules of flipping the
    top card of draw deck to become the first play card.
    """
    card = cards[id]
    animatables = SharedObjects.get_animatables()
    animatables.append(card)

    # Move card to correct position and scale
    card.instant_scale(c.DRAW_DECK_SCALE)
    card.instant_move(x=c.DRAW_DECK_CENTER_X, y=c.DRAW_DECK_CENTER_Y)

    # Slide card from draw deck to play deck (scaling appropriately)
    card.move(
        new_centerx=c.PLAY_DECK_CENTER_X,
        new_centery=c.PLAY_DECK_CENTER_Y
    )

    card.scale(
        from_scale=c.DRAW_DECK_SCALE,
        to_scale=c.PLAY_DECK_SCALE
    )


def get_focus_id():
    """
    Returns the id of the focus card. If the player has no cards,
    -1 is returned.
    """
    try:
        card = hand.cards[hand.focus_index]
    except:
        return -1

    for cid in cards:
        if cards[cid] == card:
            return cid


def next_frame():
    """
    Draws the next frame in the game. Should be called continuously at every
    framerate interval.
    """
    global clock
    surface = SharedObjects.get_surface()
    base_surface = SharedObjects.get_base_surface()
    animatables = SharedObjects.get_animatables()
    disposable_animatables = SharedObjects.get_disposable_animatables()

    # Restore background
    surface.blit(base_surface, (0, 0))

    frames = []
    for animatable in animatables:
        potential_frame = animatable.get_frame()
        if potential_frame is not None:
            frames.append(potential_frame)

    for animatable in disposable_animatables:
        potential_frame = animatable.get_frame()
        if potential_frame is not None:
            frames.append(potential_frame)

    # Draw animatables on top of background
    surface.blits(frames)

    pygame.display.update()
    clock.tick(c.FPS)


def _timer_thread(seconds):
    white = (255, 255, 255)
    red = (255, 0, 0)

    large_font = SharedObjects.get_extra_large_font()

    number = large_font.render(str(seconds), True, white)
    animatables = SharedObjects.get_animatables()

    timer = Animatable(number, (9/10)*c.WINWIDTH, (9/10)
                       * c.WINHEIGHT, hidden=False)

    animatables.append(timer)

    while seconds > 0:
        time.sleep(1)
        seconds -= 1

        if seconds <= 10:
            number = large_font.render(str(seconds), True, red)
        else:
            number = large_font.render(str(seconds), True, white)

        timer.original_surface = number
        timer.surface = number

    animatables.remove(timer)


def start_timer(seconds):
    """
    Displays a timer in the bottom right corner of the screen that counts down
    to zero.
    Parameters:
    -----------
    seconds: int value specifying how many seconds to count down from
    Returns:
    --------
    time of when timer started
    """
    now = time.time()
    threading.Thread(target=_timer_thread, args=[seconds], daemon=True).start()
    return now


def show_wildcard_wheel():
    """
    The wildward wheel is displayed in the middle of the screen.
    """
    # Check if quadrants are already being tracked in animatables. (Checking
    # just one quadrant should be sufficient)
    animatables = SharedObjects.get_animatables()
    if wildcard_quadrants[0] in animatables:
        return

    animatables.append(wildcard_background)

    cx, cy = (c.HALF_WINWIDTH, c.HALF_WINHEIGHT)
    # All quadrants will have the same dimensions
    quad_w, quad_h = wildcard_quadrants[0].rect.size

    quad_w /= 2
    quad_h /= 2

    # Position blue (top-right)
    wildcard_quadrants[0].instant_move(cx + quad_w, cy - quad_h)
    # Position blue (top-left)
    wildcard_quadrants[1].instant_move(cx - quad_w, cy - quad_h)
    # Position blue (bottom-left)
    wildcard_quadrants[2].instant_move(cx - quad_w, cy + quad_h)
    # Position blue (bottom-right)
    wildcard_quadrants[3].instant_move(cx + quad_w, cy + quad_h)

    # Start tracking quadrants in animatables
    for q in wildcard_quadrants:
        animatables.append(q)


def hide_wildcard_wheel():
    """
    The wildcard wheel is removed from the middle of the screen. Will raise an
    error if show_wildcard_wheel was not called before this function.
    """
    try:
        animatables = SharedObjects.get_animatables()
        for q in wildcard_quadrants:
            animatables.remove(q)
        animatables.remove(wildcard_background)
    except:
        raise Exception


def switch_wildcard_wheel_focus(quadrant):
    """
    The quadrant passed in move outward slightly and the rest of the quadrants
    get tucked in. There function is purely an animation and keeping track of
    which color is focused is up to the caller of this function.

    Parameters:
    -----------
    quadrant: an integer representing one of the four quadrants, which are laid
        out in the traditional mathematical way:
            0 -> Q1 (top-right)    : Blue
            1 -> Q2 (top-left)     : Red
            2 -> Q3 (bottom-left)  : Yellow
            3 -> Q4 (bottom-right) : Green
    """
    # Check for valid input
    if quadrant < 0 or quadrant > 3:
        raise Exception

    # DRY violation: this code was copied from above

    cx, cy = (c.HALF_WINWIDTH, c.HALF_WINHEIGHT)
    # All quadrants will have the same dimensions
    quad_w, quad_h = wildcard_quadrants[0].rect.size

    quad_w /= 2
    quad_h /= 2

    quad_position = [(1, -1), (-1, -1), (-1, 1), (1, 1)]

    tuck_in = set([0, 1, 2, 3])

    tuck_in = tuck_in.difference(set([quadrant]))

    for q in tuck_in:
        x, y = quad_position[q]
        wildcard_quadrants[q].move(
            new_centerx=cx + x*quad_w,
            new_centery=cy + y*quad_h,
            duration=c.SHIFT_HAND_DURATION
        )

    x, y = quad_position[quadrant]
    wildcard_quadrants[quadrant].move(
        new_centerx=cx + x*quad_w + x*c.WILDCARD_WHEEL_FOCUS_DISTANCE,
        new_centery=cy + y*quad_h + y*c.WILDCARD_WHEEL_FOCUS_DISTANCE,
        duration=c.SHIFT_HAND_DURATION
    )


def init():
    """
    Sets the background upon which all animations are drawn. Should be called
    after adding all players and cards.
    """
    global wildcard_background, wildcard_quadrants

    base_surf = SharedObjects.get_base_surface()
    large_font = SharedObjects.get_large_font()

    # Show opponent name titles
    num_opponents = len(opponents)
    for i, name in enumerate(opponents):
        # Set to xy tuple
        # xy tuple for position of opponent hand
        x = (i+1)/(num_opponents+1) * c.WINWIDTH
        y = (1/10) * c.WINHEIGHT
        opponents[name] = OpponentHand(x, y + (1/10) * c.WINHEIGHT)
        name_surf = large_font.render(name, True, (255, 255, 255))
        name_rect = name_surf.get_rect()
        name_rect.center = (x, y)
        base_surf.blit(name_surf, name_rect)

    # Show draw deck
    draw_deck = Animatable(DECK.copy())
    draw_deck.instant_scale(c.DRAW_DECK_SCALE)
    draw_deck.instant_move(c.DRAW_DECK_CENTER_X, c.DRAW_DECK_CENTER_Y)

    base_surf.blit(draw_deck.surface, draw_deck.rect)

    # Initalize wildcard wheel quadrants
    for color in [WILDWHEEL_BLUE, WILDWHEEL_RED, WILDWHEEL_YELLOW, WILDWHEEL_GREEN]:
        wildcard_quadrants.append(Animatable(color, hidden=False))
        wildcard_quadrants[-1].instant_scale(c.WILDCARD_WHEEL_SIZE)

    # Whilecard wheel background
    dim = c.WILDCARD_WHEEL_BACKGROUND_SIZE

    # Surface will be colored as border color and then filled in with
    # the background color
    background = pygame.Surface((dim, dim))
    background.fill(c.WILDCARD_BACKGROUND_BORDER_COLOR)

    t = c.WILDCARD_BORDER_THICKNESS
    interior = pygame.Surface((dim*t, dim*t))
    interior.fill(c.WILDCARD_BACKGROUND_COLOR)

    # Filling in background color
    background.blit(interior, (dim*(1-t)/2, dim*(1-t)/2))

    # Write prompt
    medium_font = SharedObjects.get_small_font()
    prompt = medium_font.render("Pick a color:", True, (255, 255, 255))
    background.blit(prompt, (dim*(1-t), dim*(1-t)))

    confirm_msg = medium_font.render(
        "press enter to select", True, (255, 255, 255))
    rect = confirm_msg.get_rect()
    # Position centered horizontally and 90% down the square
    rect.center = (dim*0.5, dim*0.9)
    background.blit(confirm_msg, rect)

    # Make the background an animatable for future drawi
    wildcard_background = Animatable(
        surface=background,
        centerx=c.HALF_WINWIDTH,
        centery=c.HALF_WINHEIGHT,
        hidden=False
    )


def transition_intro():
    ###################################################
    # Constants for Intro Scene
    ###################################################
    MAIN_CARD_SIZE = 0.6
    SECONDARY_CARD_SIZE = 0.3
    CIRCLE_CARD_SIZE = 0.2
    CIRCLE_CARD_HEIGHT = 1/4
    SPEED = 4
    NUM_CARDS = 10
    BORDER_CARD_SCALE = c.WINWIDTH*0.000125

    # Make background black
    base_surf = SharedObjects.get_base_surface()
    base_surf.fill(pygame.Color("black"))

    # Get animatables and clear any previous items
    animatables = SharedObjects.get_animatables()
    disposable_animatables = SharedObjects.get_disposable_animatables()
    animatables.clear()
    disposable_animatables.queue.clear()

    base_surf = SharedObjects.get_base_surface()

    surf = pygame.Surface((c.WINWIDTH, c.WINHEIGHT * 3/4))
    surf.fill(pygame.Color("dodgerblue3"))
    rect = surf.get_rect()
    rect.center = (c.HALF_WINWIDTH, c.HALF_WINHEIGHT)

    base_surf.blit(surf, rect)

    surf = pygame.Surface((c.WINWIDTH, c.WINHEIGHT * 3/4 * 0.95))
    surf.fill(pygame.Color("navyblue"))
    rect = surf.get_rect()
    rect.center = (c.HALF_WINWIDTH, c.HALF_WINHEIGHT)

    base_surf.blit(surf, rect)

    keys = list(CARDS.keys())

    card_w, card_h = CARDS[keys[0]].get_rect().size
    card_w *= BORDER_CARD_SCALE
    card_h *= BORDER_CARD_SCALE

    buffer = 50

    animatables = SharedObjects.get_animatables()
    disposable_animatables = SharedObjects.get_disposable_animatables()

    # Top row
    x = 0
    while x < c.WINWIDTH:
        card = Animatable(CARDS[random.choice(keys)], hidden=False)
        card.instant_scale(BORDER_CARD_SCALE)
        card.instant_move(-c.HALF_WINWIDTH * 1/8, card_h / 2)
        # base.blit(card.surface, card.rect)
        card.move(
            new_centerx=x+card_w/2,
            new_centery=card_h / 2,
            duration=1
        )
        animatables.append(card)
        x += card_w

    # Bottom row
    x = 0
    while x < c.WINWIDTH:
        card = Animatable(CARDS[random.choice(keys)], hidden=False)
        card.instant_scale(BORDER_CARD_SCALE)
        card.instant_move(c.WINWIDTH * 9/8, c.WINHEIGHT - card_h / 2)
        card.move(
            new_centerx=x+card_w/2,
            new_centery=c.WINHEIGHT - card_h / 2,
            duration=1
        )
        animatables.append(card)
        x += card_w

    keys = list(CARDS.keys())

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

        for j in range(i):
            card.move(
                new_centerx=start_x - c.WINWIDTH/2 + j + 1,
                new_centery=c.WINHEIGHT * CIRCLE_CARD_HEIGHT,
                duration=SPEED/10
            )

        for _ in range(20):
            card.move(
                new_centerx=c.HALF_WINWIDTH,
                new_centery=c.WINHEIGHT * CIRCLE_CARD_HEIGHT,
                duration=SPEED,
                steady=True
            )

            card.circle(
                c.HALF_WINWIDTH,
                c.HALF_WINHEIGHT,
                720,
                SPEED*2
            )

            card.move(
                new_centerx=c.WINWIDTH * 9/8,
                new_centery=c.WINHEIGHT * CIRCLE_CARD_HEIGHT,
                duration=SPEED,
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

        disposable_animatables.append(card)

    # Zoom in on logo animation
    logo = Animatable(DECK, hidden=False)
    logo.instant_move(c.HALF_WINWIDTH, c.HALF_WINHEIGHT)
    logo.scale(0.001, MAIN_CARD_SIZE, SPEED*2)
    disposable_animatables.append(logo)

    medium_font = SharedObjects.get_medium_font()

    # Credits text and the card it is on
    txt = medium_font.render("Credits", True, (255, 255, 255))
    start_txt = Animatable(txt, hidden=False)
    start_txt.instant_move(-c.WINWIDTH * 1/2, c.HALF_WINHEIGHT)
    start_txt.move(
        new_centerx=c.WINWIDTH * 1/4,
        new_centery=c.HALF_WINHEIGHT,
        duration=1
    )

    start_card = Animatable(BLANK, hidden=False)
    start_card.instant_scale(MAIN_CARD_SIZE)
    start_card.instant_move(-c.WINWIDTH * 1/2, c.HALF_WINHEIGHT)
    start_card.move(
        new_centerx=c.WINWIDTH * 1/4,
        new_centery=c.HALF_WINHEIGHT,
        duration=1
    )

    animatables.append(start_card)
    animatables.append(start_txt)

    # Start text and the card it is on
    txt = medium_font.render("Start", True, (255, 255, 255))
    credits_txt = Animatable(txt, hidden=False)
    credits_txt.instant_move(c.WINWIDTH * 3/2, c.HALF_WINHEIGHT)
    credits_txt.move(
        new_centerx=c.WINWIDTH * 3/4,
        new_centery=c.HALF_WINHEIGHT,
        duration=1
    )

    credits_card = Animatable(BLANK, hidden=False)
    credits_card.instant_scale(MAIN_CARD_SIZE)
    credits_card.instant_move(c.WINWIDTH * 3/2, c.HALF_WINHEIGHT)
    credits_card.move(
        new_centerx=c.WINWIDTH * 3/4,
        new_centery=c.HALF_WINHEIGHT,
        duration=1
    )

    animatables.append(credits_card)
    animatables.append(credits_txt)
