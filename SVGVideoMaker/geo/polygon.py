"""
All necessary to create, animate, and make geometry operation on Polygon.
"""

# region Imports
from SVGVideoMaker.geo.point import Point2D, Point
from SVGVideoMaker.geo.segment import Segment
from SVGVideoMaker.geo.quadrant import Quadrant
from SVGVideoMaker.geo.shape import Shape
from SVGVideoMaker.geo.animation import ModificationAnimation, AnimationType
from SVGVideoMaker.geo.utility import nearest_point, dont_match, couples
from SVGVideoMaker.geo.debug import msg, DebugLevel, DEBUG_LEVEL
# endregion Imports

class Polygon(Shape):
    """A polygon is a list of point.

    Args:
        points:
        id:
        fps:
        debug:
        use_style:
        is_fill:
        fill_color:
        is_stroke:
        stroke_color:
        stroke_width:
        opacity:
        others_rules:
    """

    p_id = 0

    def __init__(self, points, id=None, opacity=1, animation=True, style=True):
        super().__init__(id=id, animation=ModificationAnimation if animation else None, style=style, opacity=opacity)

        assert len(points) > 2, "Polygon need at less 3 points"
        if animation:
            self.animations.set_start(opacity, points)
        self.start_points = [p.copy() for p in points]
        self.points = [p.copy() for p in points] # Copy points for animation

        self.display_id = False

        if id:
            self.id = id
        else:
            self.id = Polygon.p_id
            Polygon.p_id += 1

    @classmethod
    def square(cls, start_x, start_y, side):
        """
        create a square, horizontally aligned.
        used in test scripts as a quick way to get polygons.
        """
        starting_point = Point2D(start_x, start_y)
        points = [
            Point2D(0, 0),
            Point2D(side, 0),
            Point2D(side, side),
            Point2D(0, side),
        ]
        points = [p + starting_point for p in points]
        square_polygon = cls(points)
        return square_polygon

    def get_segments(self):
        """
        iterate through all segments.
        """
        return [Segment(start, end) for start, end in couples(self.points)]

    def segments_points(self):
        """
        iterate through all segments.
        """
        return couples(self.points)

    def get_segment(self, index):
        """
        return the index segment
        """
        return [Segment(c) for c in couples(self.points)][index]

    def get_last_segment(self):
        """
        return last segment of polygon
        """
        return self.get_segment(-1)

    def area(self):
        """
        return polygon area. can be positive or negative, depending on
        orientation.
        """
        return sum(p1.cross_product(p2)
                   for p1, p2 in couples(self.points)) / 2

    def absolute_area(self):
        """
        return polygon area. Always positive
        """
        return abs(self.area())

    def is_oriented_clockwise(self):
        """
        clockwise being defined respectively to svg displayed, return
        true if polygon is oriented clockwise.
        """
        area = self.area()
        return area > 0

    def orient(self, clockwise=True):
        """
        orient polygon with given orientation
        """
        if self.is_oriented_clockwise() != clockwise:
            return Polygon(self.points[::-1])
        else:
            return self

    def get_center(self):
        """Return a point who is the center of shape.

		Returns:
			Point: The center of shape
		"""
        box = self.bounding_quadrant()
        coords = [mini + ((maxi - mini) / 2) for maxi, mini in zip(box.max_coordinates, box.min_coordinates)]
        return Point(coords)

    # region Animation
    # def apply_translation(self, value):
    #     for i in range(len(self.points)):
    #         self.points[i] += value

    def add_modification(self, frame, values):
        if self.animations:
            self.animations.add_animation(frame, AnimationType.MODIFICATION, value=values)

    def apply_modification(self, values):
        for i in range(len(self.points)):
            self.points[i] += values[i]

    def apply_inflation(self, value):
        for i in range(len(self.points)):
            self.points[i] *= value
    # endregion Animation

    # region Shape
    def reshape(self, lower_shape, bigger_shape, apply=False):
        """
        Make a new form for the animation
        The lower form is improve to match to bigger form
        :param lower_shape: the lower_shape of animation
        :param bigger_shape: the bigger_shape of animation
        :param apply: indicate if we need to apply the shape at the form
        :return: an animation who match to bigger_shape from lower_shape
        """
        matched = [-1] * len(bigger_shape)

        # Fill with nearest point
        for i, point in enumerate(bigger_shape):
            j, matched[i] = nearest_point(lower_shape, point)

        # Check if we have all lower point on matched point by distance
        # If isn't add it to keep the same shape
        pt_new_insert = []
        for low in lower_shape:
            if low not in matched:
                # Need to add this description point
                msg(f"List matched don't contain {low}, need to add !", DebugLevel.VERBOSE)

                # To do that, we search the nearest point to remove in new point area
                # and save the id to don't erase this point
                idx, _ = nearest_point(matched, low, exclude_index=pt_new_insert)
                pt_new_insert.append(idx)
                matched[idx] = low

        last_ok = -1
        test = set()

        # Force matched to match with lower_shape
        while True:

            # Check if matched shape match to lower_shape
            index, element = dont_match(matched, lower_shape, last_ok)

            # The matched match to lower_shape
            if element is True:
                break
            elif element is False:
                # Map all element after index at end/first point
                for i in range(index, len(matched)):
                    matched[i] = matched[index]
                # Clean the other point to correspond to shape
                break

            # Change already_test for this point
            if last_ok < index - 1:
                test = set()
                last_ok = index - 1

            # Find an other nearest point
            j, pt = nearest_point(lower_shape, element, test)

            # Try nearest point who aren't already test
            if pt:
                matched[index] = pt
                test.add(j)
            else:
                raise Exception("Matching shape error, we can't succeed to have a correct shape")

        if apply:
            # Save a copy to don't be affect
            # by utilisation of return
            msg("Apply reshape", DebugLevel.VERBOSE)
            self.points = list(matched)

        return matched

    def apply_shape(self, shape):
        self.points = shape

    def reset(self):
        self.animations.reset()
        self.points = [p.copy() for p in self.start_points]
    # endregion Shape

    def intersection_with(self, polygon):
        """
        return true if polygon and self
        have an intersection
        """
        from itertools import product
        for s1, s2 in product(self.get_segments(), polygon.get_segments()):
            if s1.intersection_with(s2):
                return True
        return False

    def nearest_point(self, point):
        return nearest_point(self.points, point)

    # region SVG
    def bounding_quadrant(self):
        """
        Return a quadrant who contain polygon
        :return: the quadrant who contain polygon
        """
        box = Quadrant.empty_quadrant(2)
        for point in self.points:
            box.add_point(point)
        return box

    def svg_content(self):
        """Return a string who describe the shape.

        Returns:
        	str: The string who describe the shape.
        """
        coordinates = " ".join(("{},{}".format(*p.coordinates) for p in self.points))
        string = f'<polygon points="{coordinates}" {self.get_transform()} {self.get_styles()}/>\n'
        if self.display_id:
            x_text, y_text = self.points[0].coordinates
            string += f'<text x="{x_text}" y="{y_text}">{self.id}</text>\n'

        if DEBUG_LEVEL.value <= DebugLevel.VISUAL.value:
            string += "\n".join([p.svg_content() for p in self.points]) + "\n"

        return string
    # endregion SVG

    # region Override
    def __add__(self, other):
        return Polygon([i + j for i, j in zip(self.points, other.points)])

    def __sub__(self, other):
        return Polygon([i - j for i, j in zip(self.points, other.points)])

    def __mul__(self, factor):
        return Polygon([c * factor for c in self.points])

    def __truediv__(self, factor):
        return Polygon([c / factor for c in self.points])

    def __str__(self):
        points = ",\n".join(f"\t{str(p)}" for p in self.start_points)
        return f"Polygon(id:{self.id}[\n{points}\n])"

    def __repr__(self):
        return f"{self.__class__.__name__}"
    # endregion Override

