"""
Some utility function.
"""

# region Imports
from itertools import islice, cycle
from SVGVideoMaker.geo.segment import Segment
# endregion Imports

# region Utility
def couples(iterable, turns=1):
    """Iterate on all couples of given iterable.

    This will wrap around last element.

    Args:
        iterable (iter) : The iterable to iter by couple.
        turns    (int)  : The number of iteration on all element. Default is 1 turn.

    Returns:
        iter: An iterator by couple turn's time.
    """
    return zip(iterable*turns, islice(cycle(iterable*turns), 1, None))

def dont_match(shape, shape_to_match, start_check=-1):
    """Return first point who don't match to shape_to_match.
    If match, return True, If partially match return False.

    Args:
        shape: List of points to match.
        shape_to_match: List of points who want match.
        start_check: The index to start checking.

    Returns:
        bool: True if match, False otherwise.
    """
    # Start at 0 because first end of couple is at index 1 and we increment directly
    # The first point (index 0), is check at end
    index = 0
    iter_shape = iter(shape)
    check_empty = iter(shape)

    # Iter on each segment of shape to match
    for s_match, e_match in couples(shape_to_match):
        segment = Segment(s_match, e_match)
        for point in iter_shape:
            # Increment the same iterator for empty test, if we arrive end, we can check last element
            next(check_empty, False)

            if index > start_check: # Start to check after last index ok pass in parameter
                if not segment.contains(point):
                    # Error on this point
                    return index % len(shape), e_match

            index += 1 # Increment index of good element

            if e_match == point:  # Check next segment of shape to match
                break

    shape_not_finish = False if next(check_empty, False) is False else True

    if shape_not_finish:
        # Shape is good but we have some few point who don't check
        # Indicate at user to do what he want
        # Like it's partially good, return False
        return index - 1, False
    else:
        # Shape is same, return True
        return -1, True

def nearest_point(points, point, exclude_index=None, exclude_elements=None):
    """Return nearest point of point. If exclude_index have all index return None.

    Args:
        points           (list)  : The list of points.
        point            (Point) : The point to search the nearest.
        exclude_index    (list)  : The list of index excluded.
        exclude_elements (list)  : The list of point excluded.

    Returns:
        int, point: index of point and the point
    """
    pt_id, near_pt, min_distance = -1, None, float("+inf")
    for i, pt in enumerate(points):
        # Check if the point is in exclude list
        if exclude_index and i in exclude_index:
            continue # Dont check this point

        if exclude_elements and pt in exclude_elements:
            continue # Dont check this point

        # Check if it's nearest point
        dist = pt.distance_to(point)
        if dist < min_distance:
            min_distance = dist
            pt_id, near_pt = i, pt

    return pt_id, near_pt
# endregion Utility
