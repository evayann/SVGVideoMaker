# region Imports
from itertools import islice, cycle
from geo.segment import Segment
# endregion Imports

# region Utility
def couples(iterable, turns=1):
    """
    iterate on all couples of given iterable.
    this will wrap around last element.
    """
    return zip(iterable*turns, islice(cycle(iterable*turns), 1, None))

def dont_match(shape, shape_to_match, start_check=-1):
    """
    Return first point who don't match to shape_to_match
    If match, return True, If partially match return False
    :param shape: list of points to match
    :param shape_to_match: list of points who want match
    :param start_check: the index to start checking
    :return:
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
    """
    Return nearest point of point. If exclude_index have all index return None.
    :param points:
    :param point:
    :param exclude_index:
    :param exclude_elements:
    :return:
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
