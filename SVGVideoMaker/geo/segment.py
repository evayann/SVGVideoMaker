"""
Segment between two points.
With his svg implementation.
"""

# region Imports
from SVGVideoMaker.geo.point import Point2D
from SVGVideoMaker.geo.shape import Shape
from SVGVideoMaker.geo.quadrant import Quadrant
from SVGVideoMaker.geo.ellipse import Circle
from SVGVideoMaker.geo.animation import Animation, AnimationType
# endregion Imports

class Segment(Shape):
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
    def __init__(self, start_point: Circle, end_point: Circle, id=None, opacity=1, animation=True, style=True):
        """
        create a segment from an array of two points.
        """
        super().__init__(id=id, animation=Animation if animation else None, style=style, opacity=opacity)
        if animation:
            self.set_animation_start(opacity)
        self.endpoints = [start_point, end_point]
        self.anim_points = [start_point.copy(), end_point.copy()]

    def copy(self):
        """Return duplicate of given segment.
        No shared points with original,  they are also copied.

        Returns:
            Segment : The copy of self.
        """
        return Segment(self.endpoints[0].copy(), self.endpoints[1].copy())

    def length(self):
        """Return length of segment.

        Returns:
            int : Length of segment.

        Examples:
            segment = Segment([Point([1, 1]), Point([5, 1])])
            distance = segment.length() # distance is 4
        """
        return self.endpoints[0].distance_to(self.endpoints[1])

    def get_center(self):
        """Return a point who is the center of shape.

		Returns:
			Point: The center of shape
		"""
        return self.endpoints[0] + (self.endpoints[1] - self.endpoints[0]) / 2

    # region Animation
    def reset(self):
        self.animations.reset()
        self.anim_points = [el.copy() for el in self.endpoints]

    def apply_translation(self, value):
        for i in range(len(self.anim_points)):
            self.anim_points[i] += value

    def apply_inflation(self, value):
        self.anim_points[-1] += value
    # endregion Animation

    # region SVG
    def bounding_quadrant(self):
        """Return a quadrant who contain the shape.

        Returns:
        	Quadrant: The quadrant who contain the shape.
        """
        quadrant = Quadrant.empty_quadrant(2)
        for point in self.anim_points:
            quadrant.add_point(point)
        return quadrant

    def svg_content(self):
        """Return a string who describe the shape.

        Returns:
        	str: The string who describe the shape.
        """
        return '<line x1="{}" y1="{}" x2="{}" y2="{}" {} {}/>\n'.format(
            *self.anim_points[0].coordinates,
            *self.anim_points[1].coordinates,
            self.get_transform(),
            self.get_styles())
    # endregion SVG

    def is_vertical(self):
        """Return if we are a truely vertical segment.

        Returns:
            bool : Indicate if vertical.
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
        """Return the intersection point if we have one, otherwise False

        Args:
        :param segment:
        Returns:
            bool : A boolean who indicate if we have intersection between the two segments.
        """
        start1, end1 = self.endpoints
        sx1, sy1 = start1.coordinates
        ex1, ey1 = end1.coordinates
        start2, end2 = segment.endpoints
        sx2, sy2 = start2.coordinates
        ex2, ey2 = end2.coordinates

        d = (ey2 - sy2) * (ex1 - sx1) - (ex2 - sx2) * (ey1 - sy1)
        if d:
            u_a = ((ex2 - sx2) * (sy1 - sy2) - (ey2 - sy2) * (sx1 - sx2)) / d
            u_b = ((ex1 - sx1) * (sy1 - sy2) - (ey1 - sy1) * (sx1 - sx2)) / d
        else:
            return False

        if not (0 <= u_a <= 1 and 0 <= u_b <= 1):
            return False

        return Point2D(sx1 + u_a * (ex1 - sx1), sy1 + u_a * (ey1 - sy1))

    def random_points_in(self):
        """
        Return a random point in segment.
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

    def __hash__(self):
        return hash(tuple(self.endpoints))
    # endregion Override
