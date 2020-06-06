"""
Module who contain necessary to play with style of any svg element.
"""

class Style:

	def __init__(self, fill_color=None, stroke_color=None, stroke_width=2, opacity=1, others_rules=None):
		""" Create a style for svg

		Args:
			fill_color   (str)  : The color to fill shape. Default is black.
			stroke_color (str)  : The color of stroke of the shape. Default is blue.
			stroke_width (int)  : The size of stroke of the shape. Default is 2.
			opacity      (int)  : The opacity of shape. Default is 1.
			others_rules (list) : A list of some others rules. Default is no others rules.
		"""
		# Set if we use fill, stroke, opacity... and set it
		self.fill_color = fill_color
		self.stroke_width = stroke_width
		self.stroke_color = stroke_color
		self.opacity = opacity
		self.custom = False

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

		if self.stroke_width:
			string += f'stroke-width="{self.stroke_width}" '

		if self.others_rules:
			string += " ".join(self.others_rules)

		return string
