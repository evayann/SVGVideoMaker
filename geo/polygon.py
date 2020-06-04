"""
All necessary to create, animate, and make geometry operation on Polygon.
"""

# region Imports
from geo.point import Point
from geo.segment import Segment
from geo.quadrant import Quadrant
from geo.animation import ModificationAnimation
from geo.utility import nearest_point, dont_match, couples
# endregion Imports

class Polygon(ModificationAnimation):
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

    def __init__(self, points, id=None, fps=30, debug=False, use_style=False, is_fill=False, fill_color="black",
                 is_stroke=False, stroke_color="black", stroke_width=2, opacity=1, others_rules=None):
        super().__init__(points, fps=fps, debug=debug, use_style=use_style, is_fill=is_fill, fill_color=fill_color,
                        is_stroke=is_stroke, stroke_color=stroke_color, stroke_width=stroke_width,
                        opacity=opacity, others_rules=others_rules)

        assert len(points) > 2, "Polygon need at less 3 points"
        self.start_points = points
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
        starting_point = Point([start_x, start_y])
        points = [
            Point([0.0, 0.0]),
            Point([side, 0.0]),
            Point([side, side]),
            Point([0.0, side]),
        ]
        points = [p + starting_point for p in points]
        square_polygon = cls(points)
        return square_polygon

    def segments(self):
        """
        iterate through all segments.
        """
        return map(Segment, couples(self.points))

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

    # region Animation
    def apply_translation(self, value):
        for i in range(len(self.points)):
            self.points[i] += value

    def apply_modification(self, values):
        for i in range(len(self.points)):
            self.points[i] += values[i]

    def apply_inflation(self, value):
        for i in range(len(self.points)):
            self.points[i] *= value
    # endregion Animation

    # region Shape
    def reshape(self, lower_shape: list, bigger_shape: list, apply=False):
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
                if self.verbose:
                    print(f"List matched don't contain {low}, need to add !")

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
            if self.verbose:
                print("Apply reshape")
            self.points = list(matched)

        return matched

    def apply_shape(self, shape):
        self.points = shape

    def reset(self):
        super().reset()
        self.points = [p.copy() for p in self.start_points]
    # endregion Shape

    def intersection_with(self, polygon):
        """
        return true if polygon and self
        have an intersection
        """
        from itertools import product
        for s1, s2 in product(self.segments(), polygon.segments()):
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
        """
        Return a string who describe polygon
        :return: the string who describe polygon
        """
        coordinates = " ".join(("{},{}".format(*p.coordinates) for p in self.points))
        string = f'<polygon points="{coordinates}" {self.get_styles()}/>\n'
        if self.display_id:
            x_text, y_text = self.points[0].coordinates
            string += f'<text x="{x_text}" y="{y_text}">{self.id}</text>\n'

        if self.debug:
            string += "\n".join([p.svg_content() for p in self.points]) + "\n"

        return string
    # endregion SVG

    # region Override
    def __add__(self, other):
        """
        addition operator. (useful for translations)
        """
        return Polygon([i + j for i, j in zip(self.points, other.points)])

    def __sub__(self, other):
        """
        substraction operator. (useful for translations)
        """
        return Polygon([i - j for i, j in zip(self.points, other.points)])

    def __mul__(self, factor):
        """
        multiplication by scalar operator. (useful for scaling)
        """
        return Polygon([c * factor for c in self.points])

    def __truediv__(self, factor):
        """
        division by scalar operator. (useful for scaling)
        """
        return Polygon([c / factor for c in self.points])

    def __str__(self):
        points = ",\n".join(f"\t{str(p)}" for p in self.start_points)
        return f"Polygon(id:{self.id}[\n{points}\n])\n"
    # endregion Override

