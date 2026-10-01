"""
click_detection: figures out whether a click landed on a balloon.
"""

import math


def check_pop(balloons, click_pos):
    """
    Returns the balloon that was clicked, or None if the click missed
    every balloon. A click hits when its distance from the balloon's
    center is within the balloon's radius (i.e. inside the visible circle).
    Balloons are checked topmost-first (last drawn = on top).
    """
    for balloon in reversed(balloons):
        dx = click_pos[0] - balloon.x
        dy = click_pos[1] - balloon.y
        if math.hypot(dx, dy) <= balloon.radius:
            return balloon
    return None
