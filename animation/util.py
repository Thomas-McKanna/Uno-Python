import pygame
import time
import threading

from .animatable import Animatable
from .shared_objects import SharedObjects

from . import constants as c

surface = SharedObjects.get_surface()
base_surface = SharedObjects.get_base_surface()
animatables = SharedObjects.get_animatables()
disposable_animatables = SharedObjects.get_disposable_animatables()
clock = SharedObjects.get_clock()


def next_frame():
    """
    Draws the next frame in the game. Should be called continuously at every
    framerate interval.
    """
    global clock, surface, base_surface, animatables, disposable_animatables

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

def bring_to_front(animatable):
    """
    Brings the pass in animatable to the top of the list so that it is drawn
    on top of everthing else.
    """
    SharedObjects.get_animatables().remove(animatable)
    SharedObjects.get_animatables().append(animatable)

def show_text(msg, duration, bg_color=c.MESSAGE_BACKGROUND_COLOR):
    """
    A message is shown in the middle of the screen in large font.
    Parameters:
    -----------
    msg: a str indicating the text to display
    bg_color: (R,G,B) tuple indicating background color
    duration: a float indicating the number of seconds to display the message
    """
    # Message portion
    extra_large_font = SharedObjects.get_extra_large_font()
    msg_surf = extra_large_font.render(msg, True, c.MESSAGE_TEXT_COLOR)

    msg = Animatable(msg_surf, hidden=False, chain_movements=True)

    msg.instant_move(0 - msg.rect.w / 2, c.HALF_WINHEIGHT)

    msg.move(c.HALF_WINWIDTH, c.HALF_WINHEIGHT, 1/5*duration)
    msg.move(c.HALF_WINWIDTH+1, c.HALF_WINHEIGHT, 3/5*duration)
    msg.move(c.WINWIDTH+msg.rect.w, c.HALF_WINHEIGHT, 1/5*duration)

    # Background portion
    surf = pygame.Surface((c.WINWIDTH, c.WINHEIGHT/5))
    surf.fill(bg_color)

    background = Animatable(
        surf, -c.WINWIDTH, c.HALF_WINHEIGHT, hidden=False, chain_movements=True)

    background.move(c.HALF_WINWIDTH, c.HALF_WINHEIGHT, 1/5*duration)
    background.move(c.HALF_WINWIDTH+1, c.HALF_WINHEIGHT, 3/5*duration)
    background.move(2*c.WINWIDTH, c.HALF_WINHEIGHT, 1/5*duration)

    disposable_animatables = SharedObjects.get_disposable_animatables()

    # Add background and them message to animatables
    disposable_animatables.append(background)
    disposable_animatables.append(msg)

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

    if timer in animatables:
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