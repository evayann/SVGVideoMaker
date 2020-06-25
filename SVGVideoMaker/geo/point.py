"""
Multi dimensional point and 2D point
"""

# region Imports
from SVGVideoMaker.geo.circle import Circle, X, Y
# endregion Imports

class Point(Circle):
    """
    Class who implements necessary to create and display point
    """
    def __init__(self, coordinates, id=None, opacity=1, animation=True, style=True):
        """Build a point using an array of coordinates.

        Args:
            coordinates (list) : The coordinates.
            id          (str)  : The id of shape.
            opacity     (int)  : The opacity of shape.
        """
        super().__init__(coordinates, id=id, rayon=1, opacity=opacity, animation=animation, style=style)


class Point2D(Point):
    def __init__(self, x, y, id=None, opacity=1, animation=True, style=True):
        """Build new 2D point using an array of coordinates.

        Args:
            x       (int) : Position on X - Axis
            y       (int) : Position on Y - Axis
            opacity (int) : Value of opacity
        """
        super().__init__([x, y], id=id, opacity=opacity, animation=animation, style=style)
        self.x = x
        self.y = y

    def cross_product(self, other):
        """
        Cross product between two 2d point.
        """
        return -self.y * other.x + self.x * other.y

    # region Override
    # region Math Operation
    def __add__(self, other):
        return Point2D(self.x + other.coordinates[0], self.y + other.coordinates[1])

    def __sub__(self, other):
        return Point2D(self.x - other.x, self.y - other.y)

    def __mul__(self, factor):
        return Point2D(self.x * factor, self.y * factor)

    def __truediv__(self, factor):
        return Point2D(self.x / factor, self.y / factor)

    def __abs__(self):
        return Point2D(abs(self.x), abs(self.y))

    def __eq__(self, other):
        return isinstance(other, Point2D) and self.coordinates == other.coordinates and self.rayon == other.rayon

    def __ne__(self, other):
        return not isinstance(other, Point2D) or self.coordinates != other.coordinates or self.rayon != other.rayon

    def __round__(self, n=None):
        return Point2D(round(self.x, n), round(self.y, n))
    # endregion Math Operation

    def __hash__(self):
        return hash(self.x) + hash(self.y) + hash(self.rayon)
    # endregion Override
