"""
Module who contain necessary to play with style of any svg element.
"""

class Style:

	def __init__(self, fill_color=None, stroke_color=None, stroke_width=2, stroke_linecaps=None,
	             opacity=1, others_rules=None, custom=False):
		""" Create a style for svg

		Args:
			fill_color      (str)  : The color to fill shape. Default is black.
			stroke_color    (str)  : The color of stroke of the shape. Default is blue.
			stroke_width    (int)  : The size of stroke of the shape. Default is no stroke.
			stroke_linecaps (str)  : The type of linecaps border. Default is None.
			opacity         (int)  : The opacity of shape. Default is 1.
			others_rules    (list) : A list of some others rules. Default is no others rules.
			custom          (bool) : A bool who indicate if we set a default style or if it's custom.
		"""
		self.custom = custom
		# Set if we use fill, stroke, opacity... and set it
		self.fill_color = fill_color
		self.stroke_linecaps = stroke_linecaps
		self.stroke_width = stroke_width
		self.stroke_color = stroke_color
		self.opacity = opacity

		# Others rules
		self.others_rules = []
		if others_rules:
			for rule in others_rules:
				self.others_rules.append(rule)

	def add_other_rules(self, rules):
		"""Add new rules at previous others rules.
		Can be str or list

		Args:
			rules (str or list) : The rules to add.
		"""
		if isinstance(rules, list):
			for rule in rules:
				self.others_rules.append(rule)
		else:  # str
			self.others_rules.append(rules)

	def clear_others_rules(self):
		"""
		Clear all others rules.
		"""
		self.others_rules.clear()

	def set(self, fill_color=None, stroke_color=None, stroke_width=None, stroke_linecaps=None,
	        opacity=None, custom=None):
		"""Set style of given values

		Args:
			fill_color   (str)    : The color to fill shape.
			stroke_color (str)    : The color of stroke of the shape.
			stroke_width (float)  : The size of stroke of the shape
			opacity      (float)  : The opacity of shape.
			custom       (bool)   : A bool who indicate if we set a default style or if it's custom.
		"""
		if custom:
			self.custom = custom
		if fill_color:
			self.fill_color = fill_color
		if stroke_linecaps:
			self.stroke_linecaps = stroke_linecaps
		if stroke_width is not None:
			self.stroke_width = stroke_width
		if stroke_color:
			self.stroke_color = stroke_color
		if opacity:
			self.opacity = opacity

	def get_styles(self):
		"""Get a string who describe all style.

		Returns:
			str: The string who describe style of this shape.
		"""
		string = ""

		if self.opacity:
			string += f'opacity="{self.opacity}" '

		if self.fill_color:
			string += f'fill="{self.fill_color}" '

		if self.stroke_color:
			string += f'stroke="{self.stroke_color}" '

		if self.stroke_width is not None:
			string += f'stroke-width="{self.stroke_width}" '

		if self.stroke_linecaps:
			string += f'stroke-linecap="{self.stroke_linecaps}" '

		if self.others_rules:
			string += " ".join(self.others_rules)

		return string
