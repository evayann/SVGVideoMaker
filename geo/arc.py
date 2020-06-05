
# region Imports
from geo.quadrant import Quadrant
from geo.shape import Shape
# endregion Imports

class Arc(Shape):
	def __init__(self, start, mid, end, opacity=1):
		super().__init__(start, use_style=True, is_fill=False)
		self.animations.set_start(start, opacity)
		self.start_point = start
		self.anim_point = start

		self.mid = start - mid
		self.middle_point = start - mid

		self.end = end - start
		self.end_point = end - start

		# More option for arc
		self.rot_x = 0
		self.large_arc = False
		self.invert = False

	# region Animation
	def reset(self):
		self.animations.reset()
		self.anim_point = self.start_point.copy()

	def apply_translation(self, value):
		self.anim_point += value

	def apply_inflation(self, value):
		raise Exception("Not supported yet")
	# endregion Animation

	# region SVG
	def bounding_quadrant(self):
		"""
		Return a quadrant who contain polygon
		:return: the quadrant who contain polygon
		"""
		box = Quadrant.empty_quadrant(2)
		for point in (self.anim_point, self.middle_point, self.end_point):
			box.add_point(point)
		return box

	def svg_content(self):
		"""
		Return a quadrant who contain polygon
		:return: the quadrant who contain polygon
		"""
		return f'<path d="m {"{} {}".format(*self.anim_point.coordinates)} ' \
		       f'a {"{} {}".format(*self.mid.coordinates)}' \
		       f" {self.rot_x} {1 if self.large_arc else 0} {1 if self.invert else 0}" \
		       f' {"{} {}".format(*self.end.coordinates)}" {self.get_styles()}></path>'
	# endregion SVG
