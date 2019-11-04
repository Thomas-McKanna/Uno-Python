import pygame
import time
import threading
import math

from audio.audio import *
from .animatable import Animatable
from .shared_objects import SharedObjects

from . import constants as c

surface = SharedObjects.get_surface()
base_surface = SharedObjects.get_base_surface()
animatables = SharedObjects.get_animatables()
disposable_animatables = SharedObjects.get_disposable_animatables()
clock = SharedObjects.get_clock()

timer = None
TIMER_THREAD_STOP = False
TIMER_THREAD_RUNNING = False


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
    y = c.WINHEIGHT * 1/4

    # Message portion
    extra_large_font = SharedObjects.get_extra_large_font()
    msg_surf = extra_large_font.render(msg, True, c.MESSAGE_TEXT_COLOR)

    msg = Animatable(msg_surf, hidden=False, chain_movements=True)

    msg.instant_move(0 - msg.rect.w / 2, y)

    msg.move(c.HALF_WINWIDTH, y, 1/5*duration)
    msg.move(c.HALF_WINWIDTH+1, y, 3/5*duration)
    msg.move(c.WINWIDTH+msg.rect.w, y, 1/5*duration)

    # Background portion
    surf = pygame.Surface((c.WINWIDTH, c.WINHEIGHT/5))
    surf.fill(bg_color)

    background = Animatable(
        surf, -c.WINWIDTH, y, hidden=False, chain_movements=True)

    background.move(c.HALF_WINWIDTH, y, 1/5*duration)
    background.move(c.HALF_WINWIDTH+1, y, 3/5*duration)
    background.move(2*c.WINWIDTH, y, 1/5*duration)

    disposable_animatables = SharedObjects.get_disposable_animatables()

    # Add background and them message to animatables
    disposable_animatables.append(background)
    disposable_animatables.append(msg)


def time_is_running():
    global TIMER_THREAD_RUNNING
    return TIMER_THREAD_RUNNING


def _timer_thread(seconds, cb=None):
    global timer, TIMER_THREAD_STOP, TIMER_THREAD_RUNNING

    if TIMER_THREAD_RUNNING:
        return
    else:
        TIMER_THREAD_RUNNING = True

    white = (255, 255, 255)
    red = (255, 0, 0)

    large_font = SharedObjects.get_extra_large_font()

    number = large_font.render(str(seconds), True, white)
    animatables = SharedObjects.get_animatables()

    timer = Animatable(number, (9/10)*c.WINWIDTH, (9/10)
                       * c.WINHEIGHT, hidden=False)

    animatables.append(timer)

    start_time = time.time()
    start_seconds = seconds

    broke_out = False
    while seconds > 0:
        if not TIMER_THREAD_STOP:
            sfx_timer.play()
            time.sleep(1)
            seconds = start_seconds - math.floor(time.time() - start_time)

            if seconds <= 10:
                number = large_font.render(str(seconds), True, red)
            else:
                number = large_font.render(str(seconds), True, white)

            timer.original_surface = number
            timer.surface = number
        else:
            TIMER_THREAD_STOP = False
            broke_out = True
            break

    # Run the callback
    if not broke_out and cb is not None:
        cb()

    if timer in animatables:
        animatables.remove(timer)

    TIMER_THREAD_RUNNING = False


def stop_timer():
    """
    If the timer is running, it will be removed from the screen, and the callback
    function (if it was provided), will not be called.
    """
    global TIMER_THREAD_RUNNING, TIMER_THREAD_STOP
    if TIMER_THREAD_RUNNING:
        TIMER_THREAD_STOP = True


def start_timer(seconds, cb=None):
    """
    Displays a timer in the bottom right corner of the screen that counts down
    to zero.
    Parameters:
    -----------
    seconds: int value specifying how many seconds to count down from
    cb: callback function (any parameterless function)
    Returns:
    --------
    time of when timer started
    """
    now = time.time()
    threading.Thread(target=_timer_thread, args=[
                     seconds, cb], daemon=True).start()
    return now
