
# region Imports
from SVGVideoMaker.geo.point import Point2D
from SVGVideoMaker.geo.polygon import Polygon
from SVGVideoMaker.geo.animation import ModificationAnimation
# endregion Imports

class Rectangle(Polygon):
	""" Initialize rectangle

	Args:
	    pt        (Ellipse) : The top left point of rectangle.
		width     (float)   : The width of rectangle.
		height    (float)   : The height of rectangle.
	    id        (str)     : The identifier of rectangle.
	    opacity   (int)     : The initial opacity of shape.
	    animation (bool)    : Boolean to use or not animation.
	    style     (bool)    : Boolean to use or not style.
	"""
	def __init__(self, pt, width, height, id=None, opacity=1, animation=True, style=True):
		super().__init__([pt, pt + Point2D(width, 0), pt + Point2D(width, height), pt + Point2D(0, height)],
		                 id=id, opacity=opacity, animation=ModificationAnimation if animation else None, style=style)
		self.width, self.height = width, height

	def is_in(self, pt):
		"""Return if point is in rectangle

		Args:
			pt (Point2D) : The point to check if is in rectangle.

		Returns:
			bool : A boolean to indicate if point is in rectangle.
		"""
		p1_x, p1_y, p3_x, p3_y = *self.points[0], *self.points[-2]
		return p1_x <= pt.x <= p3_x and p1_y <= pt.y <= p3_y

	# region Override
	def __iter__(self):
		"""
		Create an iterator on rectangle. Return each point of rectangle like that.
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
	""" Initialize rectangle

	Args:
	    pt        (Ellipse) : The top left point of square.
		size      (float)   : The size (width/height) of square.
	    id        (str)     : The identifier of square.
	    opacity   (int)     : The initial opacity of shape.
	    animation (bool)    : Boolean to use or not animation.
	    style     (bool)    : Boolean to use or not style.
	"""
	def __init__(self, pt, size):
		super().__init__(pt=pt, height=size, width=size)
