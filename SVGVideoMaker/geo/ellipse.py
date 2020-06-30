"""
points (any dimension).
"""
# region Imports
from math import sqrt

from SVGVideoMaker.geo.shape import Shape, X, Y
from SVGVideoMaker.geo.quadrant import Quadrant
from SVGVideoMaker.geo.animation import Animation
# endregion Imports

class Ellipse(Shape):
    """
    a point is defined as a vector of any given dimension.

    for example:

    - create a point at x=2, y=5:

    my_point = Point([2, 5])

    - find distance between two points:

    distance = point1.distance_to(point2)
    """
    def __init__(self, center, rx=10, ry=5, id=None, opacity=1, animation=True, style=True):
        """
        Instantiate a displayable ellipse
        """
        super().__init__(id=id, animation=Animation if animation else None, style=style, opacity=opacity)
        if animation:
            self.set_animation_start(opacity)
        self.start_coordinates = center
        self.coordinates = list(center) # Copy coordinates for animation
        self.rx = rx
        self.ry = ry

    def copy(self):
        """
        return copy of given point.
        """
        return Ellipse(list(self.coordinates), self.rx, self.ry)

    def distance_to(self, other):
        """
        Euclidean distance between two Ellipse center to center.
        """
        if self < other:
            return other.distance_to(self)  # we are now a symmetric function

        total = sum(((c1 - c2) ** 2 for c1, c2 in zip(self.coordinates, other.coordinates)))
        return sqrt(total)

    def get_center(self):
        """Return a point who is the center of shape.

		Returns:
			Point: The center of shape
		"""
        return self.coordinates

    def apply_translation(self, value):
        for i, v in enumerate(value.coordinates):
            self.coordinates[i] += v

    def apply_inflation(self, value):
        self.rx += value
        self.ry += value

    def reset(self):
        self.animations.reset()
        self.coordinates = list(self.start_coordinates)

    # region SVG
    def bounding_quadrant(self):
        """Return a quadrant who contain the shape.

        Returns:
        	Quadrant: The quadrant who contain the shape.
        """
        from SVGVideoMaker.geo.point import Point2D
        radius = Point2D(self.rx, self.ry)
        mini = [coord - r for coord, r in zip(self.coordinates, radius)]
        maxi = [coord + r for coord, r in zip(self.coordinates, radius)]
        return Quadrant(mini, maxi)

    def svg_content(self):
        """Return a string who describe the shape.

        Returns:
        	str: The string who describe the shape.
        """
        string = '<ellipse cx="{}" cy="{}" rx="{}" ry="{}" {} {}/>\n'
        return string.format(*self.coordinates, self.rx, self.ry, self.get_transform(), self.get_styles())
    # endregion SVG

    # region Override
    # region Math Operation
    def __add__(self, other):
        return Ellipse([i + j for i, j in zip(self.coordinates, other.coordinates)], self.rx, self.ry)

    def __sub__(self, other):
        return Ellipse([i - j for i, j in zip(self.coordinates, other.coordinates)], self.rx, self.ry)

    def __mul__(self, factor):
        return Ellipse([c * factor for c in self.coordinates], self.rx, self.ry)

    def __truediv__(self, factor):
        return Ellipse([c / factor for c in self.coordinates], self.rx, self.ry)

    def __abs__(self):
        return Ellipse([abs(c) for c in self.coordinates], self.rx, self.ry)

    def __eq__(self, other):
        return isinstance(other, Ellipse) and self.coordinates == other.coordinates and \
               self.rx == other.rx and self.ry == other.ry

    def __ne__(self, other):
        return not isinstance(other, Ellipse) or self.coordinates != other.coordinates or \
               self.rx == other.rx or self.ry == other.ry

    def __lt__(self, other):
        return self.coordinates < other.coordinates

    def __round__(self, n=None):
        return Ellipse([round(el, n) for el in self.coordinates], self.rx, self.ry)
    # endregion Math Operation

    def __str__(self):
        return f"{self.__class__.__name__}({', '.join(str(c) for c in self.coordinates)})"

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def __hash__(self):
        return sum((hash(c) for c in self.coordinates)) + hash(self.rx) + hash(self.ry)

    def __iter__(self):
        for value in self.coordinates:
            yield value
    # endregion Override

class Circle(Ellipse):
    def __init__(self, center, radius=10, id=None, opacity=1, animation=True, style=True):
        super().__init__(center, rx=radius, ry=radius, id=id,
                         opacity=opacity, animation=animation, style=style)

