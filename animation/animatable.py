import pygame
import math
import copy
from queue import Queue
from numpy import arange
from .shared_objects import SharedObjects
from .constants import FPS
from .helpers import circle_transform


class Animatable:
    def __init__(self, surface, centerx=0, centery=0, hidden=True, chain_movements=False):
        """
        Initializes an Surface for animation.
        Parameters:
        -----------
        surface: a pygame.Surface
        centerx: x-position of center of rectangle
        centery: y-position of center of rectangle
        hidden: whether or not the surface is displayed on screen
        chain_movements: if True, movements will be queued, otherwise, new
            movement requests will interrupt the current movement
        """
        self.surface = surface.copy()
        self.original_surface = surface.copy()
        self.rect = surface.get_rect()

        self.rect.centerx = centerx  # x position for top left corner
        self.rect.centery = centery  # y position for top left corner

        self.hidden = hidden

        self.chain_movements = chain_movements

        self.position_animation_queue = Queue()

        self.position_queue = Queue()

        self.rotozoom_generators = []
        self.color_generators = []

        self.current_scale = 1

    def get_frame(self):
        """
        Returns a blit pair indication what the surface is for this Animatable
        and where the surface should be displayed.
        """
        # 1. Apply transformations in scale or tilt (rotation/zoom)
        if len(self.rotozoom_generators):
            for generator in self.rotozoom_generators:
                did_trans = next(generator, False)
                if not did_trans:
                    self.rotozoom_generators = [
                        g for g in self.rotozoom_generators if not generator]

        # 2. Apply transformations of color
        if len(self.color_generators):
            for generator in self.color_generators:
                did_trans = next(generator, False)
                if not did_trans:
                    self.color_generators = [
                        g for g in self.color_generators if not generator]

        # 3. Apply changes in position
        if not self.position_queue.empty():
            self.rect.center = self.position_queue.get()
        elif not self.position_animation_queue.empty():
            args, function = self.position_animation_queue.get()
            items = function(*args)
            for item in items:
                self.position_queue.put(item)

        if not self.hidden:
            return (self.surface, self.rect)
        else:
            return None

    def hide(self):
        """
        Makes the card invisible on the screen.
        """
        self.hidden = True

    def show(self):
        """
        Makes the card visible on the screen.
        """
        self.hidden = False

    def instant_scale(self, scale):
        """
        Instantly changes the scale of the surface (no animation)
        Parameters:
        scale: proportion of original surface the surface should now be
        """
        x, y = self.rect.center

        orig_w = self.original_surface.get_rect().w
        orig_h = self.original_surface.get_rect().h
        w, h = (int(round(orig_w * scale)), int(round(orig_h * scale)))
        self.surface = pygame.transform.smoothscale(
            self.original_surface, (w, h))
        self.rect = self.surface.get_rect()
        self.instant_move(x, y)

        self.current_scale = scale

    def instant_move(self, x, y):
        """
        Instantly move the animatable to the given position.
        """
        self.rect.center = (x, y)

    def instant_color(self, RGB):
        """
        Instantly changes the color of the surface to a solid color.
        Parameters:
        -----------
        RGB: (r, g, b, a) tuple representing the color of the background (a is
            the alpha value)
        """
        original_surf = self.surface
        orig_rect = original_surf.get_rect()
        flash_surf = pygame.Surface((orig_rect.w, orig_rect.h))
        flash_surf = flash_surf.convert_alpha()
        r, g, b, a = RGB
        flash_surf.fill((r, g, b, a))
        self.surface.blit(flash_surf, (0, 0))

    def instant_rotate(self, angle):
        """
        Instantly rotates the surface by the given degree
        Parameters:
        -----------
        angle: degrees to rotate
        """
        x, y = self.rect.center
        self.surface = pygame.transform.rotate(self.surface, angle)
        self.rect = self.surface.get_rect()
        self.instant_move(x, y)

    ###########################################################################
    # Rotozoom Transformation Functions
    ###########################################################################

    def rotate(self, angle, duration):
        """
        Rotates the animatable by a number of degrees over a duration.

        This function will supercede rotate. If you want to rotate and zoom
        use the rotozoom function.

        Parameters:
        -----------
        angle: integer value; positive will rotate counter-clockwise and 
            negative will rotate clockwise
        duration: how long it seconds before the rotation completes
        """
        def generator(surface, angles):
            """
            Generator function that alters this animatable's tilt.
            """
            original_surf = surface.copy()
            for angle in angles:
                x, y = self.rect.center
                self.surface = pygame.transform.rotate(original_surf, angle)
                self.instant_move(x, y)
                yield True

        angles = [step / duration *
                  angle for step in arange(0, duration, 1 / FPS)]
        angles.append(angle)

        self.rotozoom_generators.append(generator(self.surface, angles))

    def scale(self, from_scale, to_scale, duration=0.5, pulse=False):
        """
        The animatable shrinks/grows to the given scale from a given scale

        This function will supercede rotate. If you want to rotate and zoom
        use the rotozoom function.

        Parameters:s
        -----------
        from_scale: what proportional of original surface to start scaling from
        to_scale: what proportional of original surface to scale to
        duration: how long it seconds before the rotation completes
        pulse: if True, the surface will scale to target and then scale back to
            the starting scale
        """
        def generator(surface, dimensions):
            """
            Generator function that alters this animatable's size.
            """
            original_surf = surface.copy()
            for dimension in dimensions:
                x, y = self.rect.center
                self.surface = pygame.transform.smoothscale(
                    original_surf, dimension)
                self.rect = self.surface.get_rect()
                self.instant_move(x, y)
                yield True

        if pulse:
            def scale_fun(x): return (4*from_scale - 4 *
                                      to_scale)*(x - 0.5)**2 + to_scale
        else:
            def scale_fun(x): return (from_scale - to_scale) * \
                (x - 1)**2 + to_scale

        step_size = 1 / (duration * FPS)
        steps = [
            scale_fun(x) for x in arange(0, 1, step_size)
        ]

        rect = self.original_surface.get_rect()
        w, h = (rect.w, rect.h)
        dimensions = []
        for step in steps:
            dimensions.append(
                (int(round(w * step)), int(round(h * step)))
            )
        if pulse:
            dimensions.append((int(round(w * from_scale)),
                               int(round(h * from_scale))))
        else:
            dimensions.append(
                (int(round(w * to_scale)), int(round(h * to_scale))))

        self.rotozoom_generators = []
        self.rotozoom_generators.append(
            generator(self.original_surface, dimensions))

        self.current_scale = to_scale

    def rotoscale(self, from_scale, to_scale, angle, duration):
        """
        Rotates and zooms the animatable at the same time.

        Parameters:
        -----------
        from_scale: what proportional of original surface to start scaling from
        to_scale: what proportional of original surface to scale to
        angle: integer value; positive will rotate counter-clockwise and 
            negative will rotate clockwise
        duration: how long it seconds before the rotation completes
        """
        def generator(surface, args):
            """
            Generator function that alters this animatable's size.
            """
            original_surf = surface.copy()
            for angle, scale in args:
                x, y = self.rect.center
                self.surface = pygame.transform.rotozoom(
                    original_surf, angle, scale)
                self.rect = self.surface.get_rect()
                self.instant_move(x, y)
                yield True

        angles = [step / duration *
                  angle for step in arange(0, duration, 1 / FPS)]
        angles.append(angle)

        def scale_fun(x): return (from_scale - to_scale) * \
            (x - 1)**2 + to_scale

        step_size = 1 / (duration * FPS)
        scales = [
            scale_fun(x) for x in arange(0, 1, step_size)
        ]
        scales.append(to_scale)

        args = zip(angles, scales)

        self.rotozoom_generators.append(generator(self.surface, args))

        self.current_scale = to_scale

    ###########################################################################
    # Color Transformation Functions
    ###########################################################################

    def flash(self, RGB, duration, intensity):
        """
        Flashes a surfaces, drawing the user's eye.

        This function will only work correctly if the animatable is not
        currently undergoing a rototation/zoom and if the animatable is
        a rectangle positions at a 90-degree angle.

        Parameters:
        -----------
        duration: how long in seconds the flash lasts
        intensity: how bright the surface gets; 0 - no flash, 100 - total white
        """

        def generator(surface, intensities):
            """
            Generator function that alters this animatable's surface.
            """
            original_surf = surface.copy()
            orig_rect = original_surf.get_rect()
            flash_surf = pygame.Surface((orig_rect.w, orig_rect.h))
            flash_surf = flash_surf.convert_alpha()
            r, g, b = RGB

            for intensity in intensities:
                surface.blit(original_surf, (0, 0))
                flash_surf.fill((r, g, b, intensity))
                surface.blit(flash_surf, (0, 0))
                yield True

        def flash_fun(x): return -(2*x - 1)**2 + 1

        step_size = 1 / (duration * FPS)
        steps = [
            flash_fun(x) for x in arange(0, 1, step_size)
        ]

        intensities = []
        for step in steps:
            intensities.append(intensity*step)
        intensities.append(0)

        self.color_generators.append(generator(self.surface, intensities))

    def fade_to_color(self, RGB, from_alpha, to_alpha, duration):
        """
        Fades the surface to the given RGB color tuple. The surface is not
        restored to its original color after the animation, but the original
        surface is maintained in the original_surface variable.
        Parameters:
        -----------
        RGB: (r, g, b, a) tuple indicating the color (a is an alpha value)
        duration: how long it should take for the fade to complete
        """

        def generator(alpha_vals):
            """
            Generator function that alters this animatable's surface.
            """
            original_surf = self.surface
            r, g, b = RGB
            original_surf.fill((r, g, b))      
            for val in alpha_vals:
                original_surf.set_alpha(val)
                yield True

        step_size = 1 / (duration * FPS)

        if from_alpha < to_alpha:
            minimum = from_alpha
            maximum = to_alpha
        else:
            minimum = to_alpha
            maximum = from_alpha
        
        steps = [
            (x/1) * 255 for x in arange(minimum/255, maximum/255, step_size)
        ]

        if minimum == to_alpha:
            steps.reverse()

        alpha_vals = []
        for step in steps:
            alpha_vals.append(step)
        alpha_vals.append(to_alpha)


        self.color_generators.append(generator(alpha_vals))

    ###########################################################################
    # Position-Related Animation Functions
    ###########################################################################

    def move(self, new_centerx, new_centery, duration=0.5, steady=False):
        """
        Moves a card from one position to another.
        Parameters:
        -----------
        new_x: x-coordinate of new card position (top left corner)
        new_y: y-coordinate of new card position (top left corner)
        duration: indicates how long in seconds that the
            animation should last.
        """
        rect = self.rect
        if new_centerx == rect.centerx and new_centery == rect.centery:
            # No movement required
            return None

        if not self.chain_movements:
            self.position_animation_queue = Queue()

        args = (self.surface, new_centerx, new_centery, duration, steady)
        self.position_animation_queue.put(
            (args, self._calculate_move_positions)
        )

    def _calculate_move_positions(self, surface, end_centerx, end_centery, duration, steady):
        """
        Calculates a list of positions (x-, y-coordinates) which a surface
        should take to get from one point to another.
        Parameters:
        -----------
        surface: the pygame.Surface to move
        end_centerx: the ending x-coordinate
        end_centery: the ending y-coordinate
        duration: how long in seconds that the animation should take
        """
        rect = self.rect
        start_centerx, start_centery = rect.center
        x_diff, y_diff = (start_centerx - end_centerx,
                          start_centery - end_centery)
        if x_diff == 0 and y_diff == 0:
            return []

        # Distance between the two points (start and end)
        magnitude = math.sqrt(x_diff**2 + y_diff**2)
        # Unit vector
        x_unit, y_unit = (x_diff/magnitude, y_diff/magnitude)

        # Function to determine velocity of moving surface
        if steady:
            def mvt_fun(x): return 1 - x
        else:
            def mvt_fun(x): return -x**2 + 1

        step_size = 1 / (duration * FPS)
        steps = [
            mvt_fun(x) for x in arange(0, 1 - step_size, step_size)
        ][::-1]

        positions = []
        for step in steps:
            step_x = start_centerx + (-x_unit * magnitude * step)
            step_y = start_centery + (-y_unit * magnitude * step)
            positions.append((step_x, step_y))

        return positions

    def circle(self, center_x, center_y, angle, duration=0.25):
        """
        Moves a card from one position to another.
        Parameters:
        -----------
        center_x: x-coordinate of the center of circle being rotated around
        center_x: y-coordinate of the center of circle being rotated around
        radius: how far away from the circle to rotate
        angle: how many degrees to rotate around circle
        duration: how long the animation should take
        """
        args = (center_x, center_y, angle, duration)

        if not self.chain_movements:
            self.position_animation_queue = Queue()

        self.position_animation_queue.put(
            (args, self._calculate_circle_positions)
        )

    def _calculate_circle_positions(self, center_x, center_y, angle, duration):
        """
        Calculates a list of positions (x-, y-coordinates) which a surface
        should take to move around circle.
        Parameters:
        -----------
        center_x: x-coordinate of the center of circle being rotated around
        center_x: y-coordinate of the center of circle being rotated around
        radius: how far away from the circle to rotate
        angle: how many degrees to rotate around circle
        duration: how long the animation should take
        """
        rect = self.rect
        point_x, point_y = rect.center

        angles = []
        angle_delta = (angle / duration) / FPS
        for a in arange(0, angle, angle_delta):
            angles.append(a)
        angles.append(angle)

        positions = []
        for a in angles:
            position = circle_transform(
                point_x, point_y, center_x, center_y, a)
            positions.append(position)

        return positions

    def freeze(self, duration=0.5):
            """
            Card stays in place. Useful for chained animations.
            Parameters:
            -----------
            duration: indicates how long in seconds that the
                animation should last.
            """
            if duration == 0:
                return
                
            if not self.chain_movements:
                self.position_animation_queue = Queue()

            args = (self.surface, duration)
            self.position_animation_queue.put(
                (args, self._calc_freeze_positions)
            )

    def _calc_freeze_positions(self, surface, duration):
        """
        Calculates a list of positions (x-, y-coordinates).
        """
        rect = self.rect

        step_size = 1 / (duration * FPS)

        x, y = rect.center

        positions = [
            (x, y) for i in arange(0, 1 - step_size, step_size)
        ]

        return positions