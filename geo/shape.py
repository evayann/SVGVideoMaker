"""
Implementation of necessary for shape displaying.
"""

# region Imports
from abc import abstractmethod, ABC
# endregion Imports

class Shape(ABC):
	"""
	Necessary for display shape content
	"""
	def __init__(self, debug=False, id=None, use_style=False, is_fill=False, fill_color="black",
	             is_stroke=False, stroke_color="black", stroke_width=2, opacity=1, others_rules=None):
		"""

		:param debug:
		:param use_style:
		:param is_fill:
		:param fill_color:
		:param is_stroke:
		:param stroke_color:
		:param stroke_width:
		:param opacity:
		:param others_rules:
		"""
		self.debug = debug
		self.id = id if id else self.__class__.__name__

		# Set if we use style in different shape
		self.use_style = use_style

		# Set if we use fill, stroke, opacity... and set it
		self.is_fill = is_fill
		self.fill_color = fill_color
		self.is_stroke = is_stroke
		self.stroke_color = stroke_color
		self.stroke_width = stroke_width
		self.opacity = opacity

		# Others rules
		self.others_rules = []
		if others_rules:
			for rule in others_rules:
				self.others_rules.append(rule)

	def is_style(self):
		"""Get if shape have a custom style.

		Returns:
			bool: True if shape have custom style, otherwise False.
		"""
		return self.use_style

	def get_styles(self):
		"""Get a string who describe all style.

		Returns:
			str: The string who describe style of this shape.
		"""
		string = f'opacity="{self.opacity}" '
		if self.use_style:
			if self.is_fill:
				string += f'fill="{self.fill_color}" '
			else:
				string += f'fill="none" '

			if self.is_stroke:
				string += f'stroke="{self.stroke_color}" stroke-width="{self.stroke_width}" '

			if self.others_rules:
				string += " ".join(self.others_rules)

			return string
		else:
			return string

	def get_svg(self):
		"""Return a string who describe shape only if it's visible.

		Returns:
			str: The string who describe the shape.
		"""
		return self.svg_content() if self.opacity > 0 else ""

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
