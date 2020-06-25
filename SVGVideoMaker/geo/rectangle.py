
# region Imports
from SVGVideoMaker.geo.point import Point2D
from SVGVideoMaker.geo.debug import msg, DebugLevel
from SVGVideoMaker.geo.polygon import Polygon
from SVGVideoMaker.geo.animation import ModificationAnimation
# endregion Imports

class Rectangle(Polygon):
	def __init__(self, pt=None, width=None, height=None, points=None, id=None, opacity=1, animation=True, style=True):
		# Create Rectangle by width and length
		if pt and height and width:
			pts = [pt, pt + Point2D(width, 0), pt + Point2D(0, height), pt + Point2D(width, height)]
		# Create by points position
		elif isinstance(list, points) and len(points) == 4:
			pts = points
		# Default Rectangle
		else:
			pts = [Point2D(0, 0), Point2D(1, 0), Point2D(0, 1), Point2D(1, 1)]
			msg("Bad construction of rectangle. Need a point with height and width or a list of 4 points. Instantiate a default rectangle from 0,0 to 1,1", DebugLevel.WARNING)

		super().__init__(pts, id=id, opacity=opacity, animation=ModificationAnimation if animation else None, style=style)

	def is_in(self, pt):
		"""Return if point is in rectangle

		Args:
			pt (Point2D) : The point/

		Returns:
			bool : A boolean to indicate if point is in rectangle
		"""
		p1_x, p1_y, p4_x, p4_y = *self.points[0], *self.points[-1]
		return p1_x <= pt.x <= p4_x and p1_y <= pt.y <= p4_y

	# region Override
	def __iter__(self):
		"""
		Create an iterator on rectangle. Return each point of rectangle like
		p1 ---- p2
		|       |
		|       |
		p3 ---- p4
		Yields:
			p1, p2, p3, p4
		"""
		for pt in self.points:
			yield pt
	# endregion Override

class Square(Rectangle):
	def __init__(self, position, size):
		super().__init__(pt=position, height=size, width=size)
