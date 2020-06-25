"""
Implementation of necessary for shape displaying.
"""

# region Imports
from abc import abstractmethod, ABC
from SVGVideoMaker.geo.style import Style
from SVGVideoMaker.geo.animation import Animation, ModificationAnimation
# endregion Imports

X, Y, Z = 0, 1, 2

class Shape(ABC):
	"""
	Necessary for display shape content
	"""
	COUNTER = 0

	def __init__(self, id=None, animation=None, style=False, opacity=1):
		"""Shape is an abstract class who describe main characteristics of a svg shape.

		Args:
			id (str) : The id of shape. If None default id is the name of class with a number.
		"""
		if id:
			self.id = id
		else:
			self.id = f"{self.__class__.__name__}{Shape.COUNTER}"
			Shape.COUNTER += 1

		self.animations = animation(self) if animation else None
		if style:
			self.style = Style(opacity=opacity)
		else:
			self.style = None

	# region Setters
	def set_animation_start(self, opacity, anim_type=Animation):
		if self.animations is None:
			if anim_type == Animation:
				self.animations = Animation(self)
			elif anim_type == ModificationAnimation:
				self.animations = ModificationAnimation(self)
		self.animations.set_start(opacity)

	def set_style(self, fill_color=None, stroke_color=None, stroke_width=None, stroke_linecaps=None,
	              opacity=None, others_rules=None, custom=True):
		"""Set the style of a svg element.

		Args:
			fill_color   (str)    : The color to fill shape.
			stroke_color (str)    : The color of stroke of the shape.
			stroke_width (float)  : The size of stroke of the shape.
			opacity      (float)  : The opacity of shape.
			others_rules (list)   : A list of some others rules.
			custom       (bool)   : A bool who indicate if we set a default style or if it's custom.
		"""
		if self.style is None:
			self.style = Style()
		self.style.set(fill_color, stroke_color, stroke_width, stroke_linecaps, opacity, custom)
		if others_rules:
			self.style.add_other_rules(others_rules)

	def add_other_rule(self, rules):
		"""Add new rules at previous others rules.
		Can be str or list

		Args:
			rules (str or list) : The rules to add.
		"""
		if self.style:
			self.style.add_other_rules(rules)
	# endregion Setters

	# region Getters
	def is_style(self):
		"""Get if shape have a custom style.

		Returns:
			bool: True if shape have custom style, otherwise False.
		"""
		return self.style.custom if self.style else False

	def get_styles(self):
		"""Get a string who describe all style.

		Returns:
			str: The string who describe style of this shape.
		"""
		return self.style.get_styles() if self.style else ""

	def get_svg(self):
		"""Return a string who describe shape only if it's visible.

		Returns:
			str: The string who describe the shape.
		"""
		if self.style:
			if self.style.opacity > 0:
				return self.svg_content()
			else:
				return ""
		else:
			return self.svg_content()
	# endregion Getters

	# region Animations
	@abstractmethod
	def apply_translation(self, value):
		pass

	@abstractmethod
	def apply_inflation(self, value):
		pass

	def apply_opacity(self, value):
		if self.style:
			self.style.opacity = round(self.style.opacity + value, 3)
	# endregion Animations

	# region Abstract
	@abstractmethod
	def svg_content(self):
		"""Return a string who describe the shape.

		Returns:
			str: The string who describe the shape.
		"""
		pass

	@abstractmethod
	def bounding_quadrant(self):
		"""Return a quadrant who contain the shape.

		Returns:
			Quadrant: The quadrant who contain the shape.
		"""
		pass
	# endregion Abstract

	# region Override
	def __repr__(self):
		return f"{self.__class__.__name__}"
	# endregion Override
