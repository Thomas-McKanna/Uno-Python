import pygame
import copy

from pkg_resources import resource_filename

from .animatable import Animatable
from .card import Card
from .assets import DECK
from .primary_hand import PrimaryHand
from .opponent_hand import OpponentHand
from .shared_objects import SharedObjects

from . import constants as c

# Maps id => Card
cards = {}
# Maps id => OpponentHand
opponents = {}

hand = PrimaryHand()

clock = SharedObjects.get_clock()


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

    # Restore background
    surface.blit(base_surface, (0, 0))

    frames = []
    for animatable in animatables:
        potential_frame = animatable.get_frame()
        if potential_frame is not None:
            frames.append(potential_frame)

    # Draw animatables on top of background
    surface.blits(frames)

    pygame.display.update()
    clock.tick(c.FPS)


def init():
    """
    Sets the background upon which all animations are drawn. Should be called
    after adding all players and cards.
    """
    base_surf = SharedObjects.get_base_surface()
    font = pygame.font.Font(
        resource_filename('cardanim', 'assets')
        + "/Acme-Regular.ttf", c.FONT_SIZE)

    # Show opponent name titles
    num_opponents = len(opponents)
    for i, name in enumerate(opponents):
        # Set to xy tuple
        # xy tuple for position of opponent hand
        x = (i+1)/(num_opponents+1) * c.WINWIDTH
        y = (1/10) * c.WINHEIGHT
        opponents[name] = OpponentHand(x, y + (1/10) * c.WINHEIGHT)
        name_surf = font.render(name, True, (255, 255, 255))
        name_rect = name_surf.get_rect()
        name_rect.center = (x, y)
        base_surf.blit(name_surf, name_rect)

    # Show draw deck
    draw_deck = Animatable(DECK.copy())
    draw_deck.instant_scale(c.DRAW_DECK_SCALE)
    draw_deck.instant_move(c.DRAW_DECK_CENTER_X, c.DRAW_DECK_CENTER_Y)

    base_surf.blit(draw_deck.surface, draw_deck.rect)
