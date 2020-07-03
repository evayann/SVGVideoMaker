"""
Multi dimensional point and 2D point
"""

# region Imports
from SVGVideoMaker.geo.ellipse import Circle
# endregion Imports

class Point(Circle):
    """ Initialize 2D point

        Args:
            coordinates (list of float) : List of all coordinates on differents axes of point.
            id          (str)  : The identifier of point.
            opacity     (int)  : The initial opacity of shape.
            animation   (bool) : Boolean to use or not animation.
            style       (bool) : Boolean to use or not style.
    """
    def __init__(self, coordinates, id=None, opacity=1, animation=True, style=True):
        super().__init__(coordinates, id=id, radius=1, opacity=opacity, animation=animation, style=style)


class Point2D(Point):
    """ Initialize 2D point

        Args:
            x         (float) : Position on X - Axis
            y         (float) : Position on Y - Axis
            id        (str)   : The identifier of point.
            opacity   (int)   : The initial opacity of shape.
            animation (bool)  : Boolean to use or not animation.
            style     (bool)  : Boolean to use or not style.
    """
    def __init__(self, x, y, id=None, opacity=1, animation=True, style=True):
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
        return Point2D(self.x - other.coordinates[0], self.y - other.coordinates[1])

    def __mul__(self, factor):
        return Point2D(self.x * factor, self.y * factor)

    def __truediv__(self, factor):
        return Point2D(self.x / factor, self.y / factor)

    def __abs__(self):
        return Point2D(abs(self.x), abs(self.y))

    def __round__(self, n=None):
        return Point2D(round(self.x, n), round(self.y, n))
    # endregion Math Operation

    def __hash__(self):
        return hash(self.x) + hash(self.y) + hash(self.rx) + hash(self.ry)
    # endregion Override
