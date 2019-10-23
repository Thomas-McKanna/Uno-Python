import math
from .assets import FELT

def circle_transform(point_x, point_y, center_x, center_y, angle):
    angle = math.radians(angle)
    x_origin = point_x - center_x
    y_origin = point_y - center_y
    x_prime = round(x_origin * math.cos(angle) - y_origin * math.sin(angle), 2)
    y_prime = round(y_origin * math.cos(angle) + x_origin * math.sin(angle), 2)
    return (x_prime + center_x, y_prime + center_y)

def put_felt_background(surface):
    """
    Repeats the felt texture across the surface and then returns the s˝urface.
    Parameters:
    -----------
    surface: the surface on which to put the texture
    """
    felt_w, felt_h = FELT.get_rect().size
    surf_w, surf_h = surface.get_rect().size

    x = 0
    y = 0
    while y < surf_h:
        x = 0
        while x < surf_w:
            surface.blit(FELT, (x, y))
            x += felt_w
        y += felt_h

    return surface