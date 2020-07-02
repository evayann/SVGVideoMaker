
# region Imports
from math import pi, sin, cos

from SVGVideoMaker.geo.animation import Animation, EllispePartAnimation, AnimationType
from SVGVideoMaker.geo.quadrant import Quadrant
from SVGVideoMaker.geo.debug import DEBUG_LEVEL, DebugLevel
from SVGVideoMaker.geo.point import Point2D, X, Y
from SVGVideoMaker.geo.shape import Shape
# endregion Imports


class Arc(Shape):
	def __init__(self, start, mid, end, id=None, opacity=1, animation=True, style=True):
		super().__init__(id, animation=Animation if animation else None, style=style)
		if style:
			# Set new default style
			self.set_style(fill_color="none", custom=False)
		if animation:
			self.set_animation_start(start, opacity)
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

	def get_center(self):
		"""Return a point who is the center of shape.

		Returns:
			Point: The center of shape
		"""
		return self.mid

	# region Animation
	def reset(self):
		self.animations.reset()
		self.anim_point = self.start_point.copy()

	def apply_inflation(self, value):
		raise Exception("Not supported yet")
	# endregion Animation

	# region SVG
	def bounding_quadrant(self):
		"""Return a quadrant who contain the shape.

		Returns:
			Quadrant: The quadrant who contain the shape.
		"""
		box = Quadrant.empty_quadrant(2)
		for point in (self.anim_point, self.middle_point, self.end_point):
			box.add_point(point)
		return box

	def svg_content(self):
		"""Return a string who describe the shape
		.
		Returns:
			str: The string who describe the shape.
		"""
		return f'<path d="m {"{} {}".format(*self.anim_point.coordinates)} ' \
		       f'a {"{} {}".format(*self.mid.coordinates)}' \
		       f" {self.rot_x} {1 if self.large_arc else 0} {1 if self.invert else 0}" \
		       f' {"{} {}".format(*self.end.coordinates)}" {self.get_transform()} {self.get_styles()}></path>'
	# endregion SVG

	# region Override
	def __str__(self):
		return f"{self.__class__.__name__}(Start : {self.start_point} Mid : {self.middle_point} End : {self.end_point})"
	# endregion Override

class EllipseArc(Shape):
	def __init__(self, center, radius, start_angle, end_angle, id=None, opacity=1, animation=True, style=True):
		super().__init__(id, animation=EllispePartAnimation if animation else None, style=style)
		if style:
			# Set new default style
			self.set_style(fill_color="none", custom=False)
		if animation:
			self.animations.set_start(opacity)

		# Default value, use for reset
		self.center = center
		self.radius = radius
		# Transform -90 degrees to 270 degrees...
		self.sa = start_angle % 360 if start_angle < 0 else start_angle
		self.ea = end_angle % 360 if end_angle < 0 else end_angle
		# Init point values
		self.start_point = None
		self.end_point = None

		# Value of animation
		self.center_anim = center.copy()
		self.radius_anim = radius.copy()
		self.sa_anim = self.sa
		self.ea_anim = self.ea

		# More option for arc
		self.fl = 0
		self.rot_x = 0
		self.invert = 0

		# Compute values of start and end with the given angles
		self.compute_angles()

	def compute_angles(self):
		# Compute angle and apply it to source and dest point
		rx, ry = self.radius_anim
		sr, er = -self.sa_anim * pi / 180, -self.ea_anim * pi / 180
		self.start_point = self.center_anim + Point2D(rx * cos(sr), ry * sin(sr))
		self.end_point = self.center_anim + Point2D(rx * cos(er), ry * sin(er))
		# Check if we need to invert and use large arc to keep the shape of ellipse
		self.fl = int(self.ea_anim - self.sa_anim > 180)
		self.invert = 0

	def get_center(self):
		"""Return a point who is the center of shape.

		Returns:
			Point: The center of shape
		"""
		return self.center_anim

	# region Animation
	def add_angle_translation(self, frame, value):
		"""Add translation of angles animation on shape at frame.

		Args:
			frame (int): The frame.
			value (int): The value of translation.
		"""
		if self.animations:
			self.animations.add_animation(frame, AnimationType.ANGLE_TRANSLATION, value=value)

	def add_angles(self, frame, x, y):
		"""Add modification of angles animation on shape at frame.

		Args:
			frame (int): The frame.
			x     (int): The degrees of start.
			y     (int): The degrees of end.
		"""
		if self.animations:
			self.animations.add_animation(frame, AnimationType.ANGLES, x=x, y=y)

	def reset(self):
		self.animations.reset()
		self.center_anim = self.center.copy()
		self.radius_anim = self.radius.copy()
		self.sa_anim = self.sa.copy()
		self.ea_anim = self.ea.copy()

	def apply_inflation(self, value):
		self.radius_anim += value

	def apply_angle_translation(self, angles):
		self.sa_anim += angles
		self.ea_anim += angles
		self.compute_angles()
	# endregion Animation

	# region SVG
	def bounding_quadrant(self):
		"""Return a quadrant who contain the shape.

		Returns:
			Quadrant: The quadrant who contain the shape.
		"""
		box = Quadrant.empty_quadrant(2)
		for point in (self.start_point, self.end_point):
			box.add_point(point)

		# If points isn't in the same part of trigo circle, need to get max point
		if self.ea_anim - self.sa_anim > 90:
			sa_mod, ea_mod = self.sa_anim % 360, self.ea_anim % 360
			if sa_mod <= 0 < ea_mod:
				box.add_point(self.center_anim + Point2D(self.radius_anim.coordinates[X], 0))
			if sa_mod <= 90 < ea_mod:
				box.add_point(self.center_anim + Point2D(0, -self.radius_anim.coordinates[Y]))
			if sa_mod <= 180 < ea_mod:
				box.add_point(self.center_anim + Point2D(-self.radius_anim.coordinates[X], 0))
			if sa_mod <= 270 < ea_mod:
				box.add_point(self.center_anim + Point2D(0, self.radius_anim.coordinates[Y]))

		return box

	def svg_content(self):
		"""Return a string who describe the shape.

		Returns:
			str: The string who describe the shape.
		"""
		arc = "M {sx} {sy} " \
		      "A {rx} {ry}, " \
		      "{rot_x}, {fl}, {invert}, " \
		      "{dx} {dy}"

		rx, ry = self.radius_anim
		sx, sy = self.start_point
		dx, dy = self.end_point

		arc = arc.format(sx=sx, sy=sy, rx=rx, ry=ry,
		                 rot_x=self.rot_x,
		                 fl=self.fl,
		                 invert=self.invert,
		                 dx=dx, dy=dy)

		string = f'<path d="{arc}" {self.get_transform()} {self.get_styles()}></path>'

		if DEBUG_LEVEL.value <= DebugLevel.VISUAL.value:
			string += f"{self.center_anim.svg_content()} {self.start_point.svg_content()} {self.end_point.svg_content()}"

		return string
	# endregion SVG

	# region Override
	def __str__(self):
		return f"{self.__class__.__name__}(Start : {self.start_point} Center : {self.center_anim} End : {self.end_point})"
	# endregion Override
