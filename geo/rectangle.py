
# region Imports
from geo import Point2D
from geo.animation import Animation
# endregion Imports

class Rectangle:#(Animation):
	def __init__(self, pt=None, width=None, height=None, points=None):
		# Create Rectangle by width and length
		if pt and height and width:
			# X - axis
			self.points = [pt]
			self.points.append(pt + Point2D(width, 0))

			# Y - axis
			self.points.append(pt + Point2D(0, height))
			self.points.append(pt + Point2D(width, height))
		# Create by points position
		elif isinstance(list, points) and len(points) == 4:
			self.points = points
		# Default Rectangle
		else:
			self.points = [Point2D(0, 0), Point2D(1, 0), Point2D(0, 1), Point2D(1, 1)]

	def is_in(self, pt: Point2D):
		"""
		Return if point is in rectangle
		:param pt: the point
		:return: a boolean to indicate if point is in rectangle
		"""
		p1, p4 = self.points[0], self.points[-1]
		return p1.x <= pt.x <= p4.x and p1.y <= pt.y <= p4.y

	# region Override
	def __iter__(self):
		"""
		Create an iterator on rectangle. Return each point of rectangle like
		p1 ---- p2
		|       |
		|       |
		p3 ---- p4
		:return: p1, p2, p3, p4
		"""
		for pt in self.points:
			yield pt
	# endregion Override

class Square(Rectangle):
	def __init__(self, position, size):
		super().__init__(pt=position, height=size, width=size)
