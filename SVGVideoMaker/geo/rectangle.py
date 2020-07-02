
# region Imports
from SVGVideoMaker.geo.point import Point2D
from SVGVideoMaker.geo.polygon import Polygon
from SVGVideoMaker.geo.animation import ModificationAnimation
# endregion Imports

class Rectangle(Polygon):
	def __init__(self, pt, width, height, id=None, opacity=1, animation=True, style=True):
		pts = [pt, pt + Point2D(width, 0), pt + Point2D(width, height), pt + Point2D(0, height)]
		self.width, self.height = width, height
		super().__init__(pts, id=id, opacity=opacity, animation=ModificationAnimation if animation else None, style=style)

	def is_in(self, pt):
		"""Return if point is in rectangle

		Args:
			pt (Point2D) : The point/

		Returns:
			bool : A boolean to indicate if point is in rectangle
		"""
		p1_x, p1_y, p3_x, p3_y = *self.points[0], *self.points[-2]
		return p1_x <= pt.x <= p3_x and p1_y <= pt.y <= p3_y

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
