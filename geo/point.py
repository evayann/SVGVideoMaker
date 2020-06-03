"""
Multi dimensional point and 2D point
"""

# region Imports
from geo.circle import Circle
# endregion Imports

class Point(Circle):
    """
    Class who implements necessary to create and display point
    """
    def __init__(self, coordinates, debug=False, use_style=False, is_fill=False, fill_color="black",
	             is_stroke=False, stroke_color="black", stroke_width=2, opacity=1, others_rules=None):
        """
        build new point using an array of coordinates.
        """
        super().__init__(coordinates, debug, use_style, is_fill, fill_color,
                       is_stroke, stroke_color, stroke_width, opacity, others_rules)
        self.rayon = 1


class Point2D(Circle):
    def __init__(self, x, y, debug=False, use_style=False, is_fill=False, fill_color="black",
                 is_stroke=False, stroke_color="black", stroke_width=2, opacity=1, others_rules=None):
        """
		build new 2D point using an array of coordinates.
		"""
        super().__init__([x, y], debug, use_style, is_fill, fill_color,
                         is_stroke, stroke_color, stroke_width, opacity, others_rules)
        self.rayon = 1
        self.x = x
        self.y = y

    def cross_product(self, other):
        """
        cross product between 2 2d point
        """
        return -self.y * other.x + self.x * other.y

    # region Override
    # region Math Operation
    def __add__(self, other):
        """
        addition operator. (useful for translations)
        """
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """
        substraction operator. (useful for translations)
        """
        return Point2D(self.x - other.x, self.y - other.y)

    def __mul__(self, factor):
        """
        multiplication by scalar operator. (useful for scaling)
        """
        return Point2D(self.x * factor, self.y * factor)

    def __truediv__(self, factor):
        """
        division by scalar operator. (useful for scaling)
        """
        return Point2D(self.x / factor, self.y / factor)

    def __abs__(self):
        return Point2D(abs(self.x), abs(self.y))

    def __eq__(self, other):
        return isinstance(other, Point2D) and self.coordinates == other.coordinates and self.rayon == other.rayon

    def __ne__(self, other):
        return not isinstance(other, Point2D) or self.coordinates != other.coordinates or self.rayon != other.rayon
    # endregion Math Operation

    def __hash__(self):
        return hash(self.x) + hash(self.y) + hash(self.rayon)
    # endregion Override
