"""
Segment between two points.
With his svg implementation.
"""

# region Imports
from geo.point import Point2D
from geo.animation import Animation
from geo.quadrant import Quadrant
from geo.circle import Circle
# endregion Imports

class Segment(Animation):
    """
    oriented segment between two points.

    for example:

    - create a new segment between two points:

        segment = Segment([point1, point2])

    - create a new segment from coordinates:

        segment = Segment([Point([1.0, 2.0]), Point([3.0, 4.0])])

    - compute intersection point with other segment:

        intersection = segment1.intersection_with(segment2)

    """
    def __init__(self, start_point: Circle, end_point: Circle,
                 fps=30, verbose=False,
                 debug=False, id=None, use_style=False, is_fill=False, fill_color="black",
                 is_stroke=False, stroke_color="black", stroke_width=2, opacity=1, others_rules=None):
        """
        create a segment from an array of two points.
        """
        super().__init__([start_point, end_point], fps=fps, verbose=verbose, debug=debug, id=id, use_style=use_style,
                         is_fill=is_fill, fill_color=fill_color,
                         is_stroke=is_stroke, stroke_color=stroke_color, stroke_width=stroke_width,
                         opacity=opacity, others_rules=others_rules)
        self.endpoints = [start_point, end_point]
        self.anim_points = [start_point.copy(), end_point.copy()]

    def copy(self):
        """
        return duplicate of given segment (no shared points with original,
        they are also copied).
        """
        return Segment(self.endpoints[0].copy(), self.endpoints[1].copy())

    def length(self):
        """
        return length of segment.
        example:
            segment = Segment([Point([1, 1]), Point([5, 1])])
            distance = segment.length() # distance is 4
        """
        return self.endpoints[0].distance_to(self.endpoints[1])

    # region Animation
    def reset(self):
        super().reset()
        self.anim_points = [el.copy() for el in self.endpoints]

    def apply_translation(self, value):
        for i in range(len(self.anim_points)):
            self.anim_points[i] += value

    def apply_inflation(self, value):
        """
        Inflation is to move only end point
        :param value:
        :return:
        """
        self.anim_points[-1] += value
    # endregion Animation

    # region SVG
    def bounding_quadrant(self):
        """
        return min quadrant containing self.
        """
        quadrant = Quadrant.empty_quadrant(2)
        for point in self.anim_points:
            quadrant.add_point(point)
        return quadrant

    def svg_content(self):
        """
        svg for tycat.
        """
        return '<line x1="{}" y1="{}" x2="{}" y2="{}" {}/>\n'.format(
            *self.anim_points[0].coordinates,
            *self.anim_points[1].coordinates,
            self.get_styles())
    # endregion SVG

    def is_vertical(self):
        """
        return if we are a truely vertical segment.
        """
        return self.endpoints[0].coordinates[0] == self.endpoints[1].coordinates[0]

    def endpoint_not(self, point):
        """
        return first endpoint which is not given point.
        """
        if self.endpoints[0] == point:
            return self.endpoints[1]

        return self.endpoints[0]

    def contains(self, possible_point):
        """
        is given point inside us ?
        be careful, determining if a point is inside a segment is a difficult problem
        (it is in fact a meaningless question in most cases).
        you might get wrong results for points extremely near endpoints.
        """
        distance = sum(possible_point.distance_to(p) for p in self.endpoints)
        return abs(distance - self.length()) < 0.000001

    def parallels(self, segment):
        """
        return true if segment are parallels
        although false
        """
        return self.endpoints[0].cross_product(self.endpoints[1]) == \
               segment.endpoints[0].cross_product(segment.endpoints[1]) == 0

    def intersection_with(self, segment):
        """
        return true if segment and self
        have an intersection
        """
        on_segment = lambda p, q, r: min(p.x, r.x) <= q.x <= max(p.x, r.x) and min(p.y, r.y) <= q.y <= max(p.y, r.y)
        def orientation(p, p1, p2):
            val = (p1.y - p.y) * (p2.x - p1.x) - (p1.x - p.x) * (p2.y - p1.y)
            if val == 0:
                return 0 # colinear
            return 1 if val > 0 else 2 # clock or counterclock wise

        p1, q1 = self.endpoints
        p2, q2 = segment.endpoints

        o1 = orientation(p1, q1, p2)
        o2 = orientation(p1, q1, q2)
        o3 = orientation(p2, q2, p1)
        o4 = orientation(p2, q2, q1)

        if (o1 != o2 and o3 != o4) or (o1 == 0 and on_segment(p1, p2, q1)) or (o2 == 0 and on_segment(p1, q2, q1)) \
            or (o3 == 0 and on_segment(p2, p1, q2)) or (o4 == 0 and on_segment(p2, q1, q2)):
            return True

        return False

    def intersect_point(self, segment):
        """
        Return the parameter point if we have one, otherwise False
        :param segment:
        :return:
        """
        start1, end1 = self.endpoints
        start2, end2 = segment.endpoints

        d = (end2.y - start2.y) * (end1.x - start1.x) - (end2.x - start2.x) * (end1.y - start1.y)
        if d:
            uA = ((end2.x - start2.x) * (start1.y - start2.y) - (end2.y - start2.y) * (start1.x - start2.x)) / d
            uB = ((end1.x - start1.x) * (start1.y - start2.y) - (end1.y - start1.y) * (start1.x - start2.x)) / d
        else:
            return False

        if not (0 <= uA <= 1 and 0 <= uB <= 1):
            return False

        return Point2D(start1.x + uA * (end1.x - start1.x), start1.y + uA * (end1.y - start1.y))

    def random_points_in(self):
        """
        return a random point in segment
        """
        from random import random
        t, p1, p2 = random(), self.endpoints[0], self.endpoints[1]
        return p1.x + t * (p2.x - p1.x), p1.y + t * (p2.y - p1.y)

    # region Override
    def __len__(self):
        return self.length()

    def __eq__(self, other):
        return self.endpoints == other.endpoints

    def __str__(self):
        return "Segment([" + str(self.endpoints[0]) + ", " + \
               str(self.endpoints[1]) + "])"

    def __repr__(self):
        return "[" + repr(self.endpoints[0]) + ", " + \
               repr(self.endpoints[1]) + "])"

    def __hash__(self):
        return hash(tuple(self.endpoints))
    # endregion Override
